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
@click.option("--url", required=True, envvar="ADDJ_URL")
@click.option("--username", required=True, envvar="ADDJ_USERNAME")
@click.option("--password", required=True, envvar="ADDJ_PASSWORD")
@click.pass_context
def main(context: click.Context, url: str, username: str, password: str):
    context.ensure_object(dict)
    context.obj["url"] = url
    context.obj["username"] = username
    context.obj["password"] = password


@main.command("PlayoutONE")
@click.option("--db-server", required=True, envvar="PLAYOUT_SYNC_SERVER")
@click.option("--database", required=True, envvar="PLAYOUT_SYNC_DATABASE")
@click.option("--db-username", required=True, envvar="PLAYOUT_SYNC_USERNAME")
@click.option("--db-password", required=True, envvar="PLAYOUT_SYNC_PASSWORD")
@click.option("--logging-config", default="logging.ini")
@click.pass_context
def playout_one(
    context: click.Context,
    server: str,
    db_server: str,
    db_username: str,
    db_password: str,
    logging_config: str,
):
    """Import data from PlayoutONE.

    Args:
        db_server (str): The SQL server to connect to.
        database (str): The SQL database name.
        db_username (str): The SQL username.
        db_password (str): The SQL password.
    """
    logger = _get_logger(logging_config)

    cart_type_repo = PlayoutOneCartTypeRepository(
        logger, db_server, database, db_username, db_password
    )
    cart_type_repo.get_all()


if __name__ == "__main__":
    main()
