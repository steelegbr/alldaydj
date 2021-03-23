import click
from typing import List

PLAYOUT_SYSTEMS: List[str] = ["PlayoutONE", "AutoTrack"]


@click.group()
def main():
    pass


@main.command("PlayoutONE")
@click.option("--server", required=True, envvar="PLAYOUT_SYNC_SERVER")
@click.option("--database", required=True, envvar="PLAYOUT_SYNC_DATABASE")
@click.option("--username", required=True, envvar="PLAYOUT_SYNC_USERNAME")
@click.option("--password", required=True, envvar="PLAYOUT_SYNC_PASSWORD")
def playout_one(server, database, username, password):
    pass


if __name__ == "__main__":
    main()
