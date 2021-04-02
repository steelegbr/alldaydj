from alldaydj.http import Authenticator
from asyncio import gather, get_event_loop
import click
from logging import getLogger, Logger
from logging.config import fileConfig
from typing import List
from repositories.cart_type import (
    AllDayDjCartTypeRepository,
    CartTypeRepository,
    PlayoutOneCartTypeRepository,
)

PLAYOUT_SYSTEMS: List[str] = ["PlayoutONE", "AutoTrack"]


def _get_logger(logger_file: str) -> Logger:
    fileConfig(logger_file)
    return getLogger(__name__)


def sync(
    logger: Logger, src_type_repo: CartTypeRepository, dst_type_repo: CartTypeRepository
):

    event_loop = get_event_loop()

    src_types = event_loop.run_until_complete(src_type_repo.get_all())
    dst_types = event_loop.run_until_complete(dst_type_repo.get_all())

    dst_type_names = [cart_type.name for cart_type in dst_types]

    missing_types = [
        cart_type for cart_type in src_types if cart_type.name not in dst_type_names
    ]

    logger.info(
        f"Found {len(missing_types)} cart type(s) missing from the destination."
    )


@click.group()
@click.option("--url", required=True, envvar="ADDJ_SYNC_URL")
@click.option("--username", required=True, envvar="ADDJ_SYNC_USERNAME")
@click.option("--password", required=True, envvar="ADDJ_SYNC_PASSWORD")
@click.option("--secure/--insecure", default=False)
@click.pass_context
def main(context: click.Context, url: str, username: str, password: str, secure: bool):
    context.ensure_object(dict)
    context.obj["url"] = url
    context.obj["username"] = username
    context.obj["password"] = password
    context.obj["secure"] = secure


@main.command("PlayoutONE")
@click.option("--db-server", required=True, envvar="PLAYOUT_SYNC_SERVER")
@click.option("--database", required=True, envvar="PLAYOUT_SYNC_DATABASE")
@click.option("--db-username", required=True, envvar="PLAYOUT_SYNC_USERNAME")
@click.option("--db-password", required=True, envvar="PLAYOUT_SYNC_PASSWORD")
@click.option("--logging-config", default="logging.ini")
@click.pass_context
def playout_one(
    context: click.Context,
    db_server: str,
    database: str,
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

    authenticator = Authenticator.instance(
        context.obj["secure"],
        context.obj["url"],
        context.obj["username"],
        context.obj["password"],
        logger,
    )

    src_cart_type_repo = PlayoutOneCartTypeRepository(
        logger, db_server, database, db_username, db_password
    )

    dst_cart_type_repo = AllDayDjCartTypeRepository(
        authenticator, logger, context.obj["url"], context.obj["secure"]
    )

    sync(logger, src_cart_type_repo, dst_cart_type_repo)


if __name__ == "__main__":
    main()
