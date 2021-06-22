from functools import lru_cache
from os import makedirs
from os.path import exists
from typing import Any, Dict, List

from rich.progress import track
from slugify import slugify

from adapters import OxwallDB
from model import Post, Topic, User


def export(oxwall: OxwallDB, directory: str) -> None:
    """Export the Oxwall data into json files."""
    for topic_data in track(oxwall.topics()):
        topic = Topic(
            id=topic_data["id"],
            title=topic_data["title"],
            views=topic_data["views"],
            project=topic_data["project"],
            group=topic_data["group"],
            user=User(
                id=topic_data["user_id"],
                name=topic_data["username"],
                email=topic_data["email"],
            ),
            posts=_get_posts(oxwall.posts(topic_data["id"])),
        )

        topic_directory = f"{directory}/{topic.project}/{topic.group}"

        if not exists(topic_directory):
            makedirs(topic_directory)

        with open(
            f"{topic_directory}/{slugify(topic.title)}.json", "w+"
        ) as file_descriptor:
            file_descriptor.write(topic.json(indent=2))


def _get_posts(posts_data: List[Dict[str, Any]]) -> List[Post]:
    return [
        Post(
            id=post_data["id"],
            text=post_data["text"],
            user=User(
                id=post_data["user_id"],
                name=post_data["username"],
                email=post_data["email"],
            ),
        )
        for post_data in posts_data
    ]
