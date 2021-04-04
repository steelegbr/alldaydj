from alldaydj.http import Authenticator
from asyncio import as_completed, run
import click
from logging import getLogger, Logger
from logging.config import fileConfig
from typing import List
from repositories.cart import CartRepository, PlayoutOneCartRepository
from repositories.cart_type import (
    AllDayDjCartTypeRepository,
    CartTypeRepository,
    PlayoutOneCartTypeRepository,
)


PLAYOUT_SYSTEMS: List[str] = ["PlayoutONE", "AutoTrack"]


def _get_logger(logger_file: str) -> Logger:
    """Configure the logger from file.

    Args:
        logger_file (str): The configuration file.

    Returns:
        Logger: The configured logger.
    """
    fileConfig(logger_file)
    return getLogger(__name__)


async def sync_cart_types(
    logger: Logger, src_type_repo: CartTypeRepository, dst_type_repo: CartTypeRepository
) -> List[bool]:
    """Synchronises cart types.

    Args:
        logger (Logger): The logger to record into.
        src_type_repo (CartTypeRepository): The source cart type repository.
        dst_type_repo (CartTypeRepository): The destination cart type repository.

    Returns:
        List[bool]: A list of True/False values indicating how successful the synchronisation was.
    """
    src_types = await src_type_repo.get_all()
    dst_types = await dst_type_repo.get_all()

    dst_type_names = [cart_type.name for cart_type in dst_types]

    missing_types = [
        cart_type for cart_type in src_types if cart_type.name not in dst_type_names
    ]

    logger.info(
        f"Found {len(missing_types)} cart type(s) missing from the destination."
    )

    missing_type_tasks = [dst_type_repo.save(cart_type) for cart_type in missing_types]
    missing_type_save_results = []
    for missing_type_task in as_completed(missing_type_tasks):
        missing_type_save_results.append(await missing_type_task)

    return missing_type_save_results


async def sync(
    logger: Logger,
    src_type_repo: CartTypeRepository,
    dst_type_repo: CartTypeRepository,
    src_cart_repo: CartRepository,
):

    missing_type_sync_results = await sync_cart_types(
        logger, src_type_repo, dst_type_repo
    )
    if all(missing_type_sync_results):
        logger.info(
            f"Added {len(missing_type_sync_results)} cart type(s) to the destination."
        )
    else:
        logger.error(
            f"Added {sum(missing_type_sync_results)} of {len(missing_type_sync_results)} cart type(s) to the destination."
        )
        return

    await src_cart_repo.get_all()


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

    src_cart_repo = PlayoutOneCartRepository(
        logger, db_server, database, db_username, db_password
    )

    run(sync(logger, src_cart_type_repo, dst_cart_type_repo, src_cart_repo))


if __name__ == "__main__":
    main()
