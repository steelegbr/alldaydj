"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from alldaydj.http import Authenticator
from asyncio import as_completed, run
import click
from logging import getLogger, Logger
from logging.config import fileConfig
from typing import List
from repositories.cart import (
    AllDayDjCartRepository,
    Cart,
    CartRepository,
    PlayoutOneCartRepository,
)
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


async def sync_cart_data(
    logger: Logger, cart: Cart, dst_cart_repo: CartRepository
) -> bool:
    existing = await dst_cart_repo.get_by_label(cart.label)
    if not existing:
        return await dst_cart_repo.save_new(cart)

    # Work out if/what we need to update

    new_dict = dst_cart_repo.cart_to_dictionary(cart)
    differences = {}
    for key, value in new_dict.items():
        if value and not existing[key] == value:
            differences[key] = value

    if differences:
        return await dst_cart_repo.update(differences, existing["id"])

    logger.info(f"No changes required for cart {cart.label}.")
    return False


async def sync_cart_audio(
    logger: Logger,
    cart: Cart,
    src_cart_repo: CartRepository,
    dst_cart_repo: CartRepository,
) -> bool:

    file_path = src_cart_repo.get_file_path(cart)
    if not file_path:
        logger.warning(f"Failed to find the audio file for cart {cart.label}.")
        return False

    existing_cart = await dst_cart_repo.get_by_label(cart.label)
    if not existing_cart:
        logger.warning(
            f"Failed to find cart {cart.label} in the destination system to upload audio to."
        )
        return False

    return await dst_cart_repo.upload_audio(existing_cart["id"], file_path)


async def sync_cart(
    logger: Logger,
    cart: Cart,
    src_cart_repo: CartRepository,
    dst_cart_repo: CartRepository,
    force_audio_update: bool,
) -> bool:

    data_updated = await sync_cart_data(logger, cart, dst_cart_repo)
    if force_audio_update or data_updated:
        return await sync_cart_audio(logger, cart, src_cart_repo, dst_cart_repo)

    return data_updated


async def sync_carts(
    logger: Logger,
    src_cart_repo: CartRepository,
    dst_cart_repo: CartRepository,
    force_audio_update: bool,
):

    carts = await src_cart_repo.get_all()
    sync_cart_tasks = [
        sync_cart(logger, cart, src_cart_repo, dst_cart_repo, force_audio_update)
        for cart in carts
    ]
    sync_cart_results = []

    for sync_cart_task in as_completed(sync_cart_tasks):
        try:
            result = await sync_cart_task
        except Exception as ex:
            logger.error(ex)
            result = False
        sync_cart_results.append(result)

    logger.info(
        f"Successfully synchronised {sum(sync_cart_results)} of {len(sync_cart_results)} carts."
    )


async def sync(
    logger: Logger,
    src_type_repo: CartTypeRepository,
    dst_type_repo: CartTypeRepository,
    src_cart_repo: CartRepository,
    dst_cart_repo: CartRepository,
    force_audio_update: bool,
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

    await sync_carts(logger, src_cart_repo, dst_cart_repo, force_audio_update)


@click.group()
@click.option("--url", required=True, envvar="ADDJ_SYNC_URL")
@click.option("--username", required=True, envvar="ADDJ_SYNC_USERNAME")
@click.option("--password", required=True, envvar="ADDJ_SYNC_PASSWORD")
@click.option("--secure/--insecure", default=False)
@click.option("--force-audio-update/--no-force-audio-update", default=False)
@click.pass_context
def main(
    context: click.Context,
    url: str,
    username: str,
    password: str,
    secure: bool,
    force_audio_update: bool,
):
    context.ensure_object(dict)
    context.obj["url"] = url
    context.obj["username"] = username
    context.obj["password"] = password
    context.obj["secure"] = secure
    context.obj["force_audio_update"] = force_audio_update


@main.command("PlayoutONE")
@click.option("--db-server", required=True, envvar="PLAYOUT_SYNC_SERVER")
@click.option("--database", required=True, envvar="PLAYOUT_SYNC_DATABASE")
@click.option("--db-username", required=True, envvar="PLAYOUT_SYNC_USERNAME")
@click.option("--db-password", required=True, envvar="PLAYOUT_SYNC_PASSWORD")
@click.option("--file-path", required=True, envvar="PLAYOUT_SYNC_FILE_PATH")
@click.option("--logging-config", default="logging.ini")
@click.pass_context
def playout_one(
    context: click.Context,
    db_server: str,
    database: str,
    db_username: str,
    db_password: str,
    file_path: str,
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
        logger, db_server, database, db_username, db_password, file_path
    )

    dst_cart_repo = AllDayDjCartRepository(
        authenticator, logger, context.obj["url"], context.obj["secure"]
    )

    run(
        sync(
            logger,
            src_cart_type_repo,
            dst_cart_type_repo,
            src_cart_repo,
            dst_cart_repo,
            context.obj["force_audio_update"],
        )
    )


if __name__ == "__main__":
    main()
