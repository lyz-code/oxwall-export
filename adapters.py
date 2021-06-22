from typing import Any, Dict, List

import html2text
from mysql.connector import connect
from slugify import slugify


class OxwallDB:
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        self.connection = connect(
            host=host, port=3306, user=user, password=password, database=database
        )

    def topics(self) -> List[Dict[str, Any]]:
        topics = []
        topics_cursor = self.connection.cursor()
        topics_cursor.execute(
            """
            SELECT
                topic.id,
                topic.title,
                topic.viewCount,
                user.id as user_id,
                user.username,
                user.email,
                project.title as project,
                topic_group.title as 'group'
            FROM ow_forum_topic as topic
            LEFT JOIN ow_base_user as user
            ON topic.userId = user.id
            LEFT JOIN ow_projects_project as project
            ON topic.projectId = project.id
            LEFT JOIN ow_groups_group as topic_group
            ON topic.groupId = topic_group.id
            """
        )
        for record in topics_cursor:
            try:
                group = slugify(record[7])
            except TypeError:
                group = "None"

            topics.append(
                {
                    "id": record[0],
                    "title": record[1],
                    "views": record[2],
                    "user_id": record[3],
                    "username": record[4],
                    "email": record[5],
                    "project": slugify(record[6]),
                    "group": group,
                }
            )
        return topics

    def posts(self, topic_id: int) -> List[Dict[str, Any]]:
        posts = []

        cursor = self.connection.cursor()
        cursor.execute(
            f"""
            SELECT
                post.id,
                post.text,
                user.id as user_id,
                user.username,
                user.email
            FROM ow_forum_post as post
            LEFT JOIN ow_base_user as user
            ON post.userId = user.id
            WHERE topicID = '{topic_id}'"""
        )
        for record in cursor:
            posts.append(
                {
                    "id": record[0],
                    "text": html2text.html2text(record[1]),
                    "user_id": record[2],
                    "username": record[3],
                    "email": record[4],
                }
            )
        return posts
