import click
from logging import getLogger, Logger
from logging.config import fileConfig
from typing import List
from repositories.cart_type import PlayoutOneCartTypeRepository

PLAYOUT_SYSTEMS: List[str] = ["PlayoutONE", "AutoTrack"]


def _get_logger(logger_file: str) -> Logger:
    fileConfig(logger_file)
    return getLogger(__name__)


@click.group()
def main():
    pass


@main.command("PlayoutONE")
@click.option("--server", required=True, envvar="PLAYOUT_SYNC_SERVER")
@click.option("--database", required=True, envvar="PLAYOUT_SYNC_DATABASE")
@click.option("--username", required=True, envvar="PLAYOUT_SYNC_USERNAME")
@click.option("--password", required=True, envvar="PLAYOUT_SYNC_PASSWORD")
@click.option("--logging-config", default="logging.ini")
def playout_one(
    server: str, database: str, username: str, password: str, logging_config: str
):
    """Import data from PlayoutONE.

    Args:
        server (str): The SQL server to connect to.
        database (str): The SQL database name.
        username (str): The SQL username.
        password (str): The SQL password.
    """
    logger = _get_logger(logging_config)

    cart_type_repo = PlayoutOneCartTypeRepository(
        logger, server, database, username, password
    )
    cart_type_repo.get_all()


if __name__ == "__main__":
    main()
