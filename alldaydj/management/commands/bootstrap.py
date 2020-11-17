"""
    AllDay DJ Boostrap CLI command.
"""

from alldaydj.tasks import bootstrap
from django.core.management.base import BaseCommand, CommandError, CommandParser
from email.utils import parseaddr
import re
from typing import Any, Optional


class Command(BaseCommand):
    """
    The boostrap command.
    """

    help = "Perform the initial public tenancy bootstrap"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("tenancy", type=str)
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:

        tenancy = options["tenancy"]
        username = options["username"]
        password = options["password"]

        # Sanity checks

        if not re.match("[a-zA-Z]|[a-zA-Z][a-zA-Z0-9]*[a-zA-Z0-9]", tenancy):
            raise ValueError(
                f"{tenancy} is not a valid tenancy name. It must match hostname rules without dashes!"
            )

        if not username or not password:
            raise ValueError(
                "You must supply a username and password for the initial setup."
            )

        (_, email) = parseaddr(username)
        if not email:
            raise ValueError(f"{email} is not a valid e-mail address.")

        #  Perform the bootstrap

        bootstrap.apply_async(args=(tenancy, username, password))
