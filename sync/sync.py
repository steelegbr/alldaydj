import click
from logging import DEBUG, getLogger, StreamHandler
from typing import List
from repositories.cart_type import PlayoutOneCartTypeRepository

PLAYOUT_SYSTEMS: List[str] = ["PlayoutONE", "AutoTrack"]
LOGGER = getLogger(__name__)
LOGGER.setLevel(DEBUG)
HANDLER = StreamHandler()
HANDLER.setLevel(DEBUG)
LOGGER.addHandler(HANDLER)


@click.group()
def main():
    pass


@main.command("PlayoutONE")
@click.option("--server", required=True, envvar="PLAYOUT_SYNC_SERVER")
@click.option("--database", required=True, envvar="PLAYOUT_SYNC_DATABASE")
@click.option("--username", required=True, envvar="PLAYOUT_SYNC_USERNAME")
@click.option("--password", required=True, envvar="PLAYOUT_SYNC_PASSWORD")
def playout_one(server: str, database: str, username: str, password: str):
    """Import data from PlayoutONE.

    Args:
        server (str): The SQL server to connect to.
        database (str): The SQL database name.
        username (str): The SQL username.
        password (str): The SQL password.
    """
    cart_type_repo = PlayoutOneCartTypeRepository(
        LOGGER, server, database, username, password
    )
    cart_type_repo.get_all()


if __name__ == "__main__":
    main()
