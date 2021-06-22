from os import makedirs
from os.path import exists

from rich.prompt import Prompt

from adapters import OxwallDB
from services import export


def cli() -> None:
    host = Prompt.ask("MySQL Host: ")
    user = Prompt.ask("MySQL User: ")
    database = Prompt.ask("MySQL Database: ")
    password = Prompt.ask("MySQL Password: ", password=True)
    directory = "out"

    oxwall = OxwallDB(host=host, user=user, password=password, database=database)

    if not exists(directory):
        makedirs(directory)

    export(oxwall, directory)


if __name__ == "__main__":
    cli()
