"""
    AllDay DJ Tenant User Creation
"""

from alldaydj.tasks import create_user
from django.core.management.base import BaseCommand, CommandError, CommandParser
from email.utils import parseaddr
import re
from typing import Any, Optional


class Command(BaseCommand):
    """
    Creates a tenant user.
    """

    help = "Creates a tenant user"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:

        username = options["username"]
        password = options["password"]

        # Sanity checks

        if not username or not password:
            raise CommandError(
                "You must supply a username and password for the user."
            )

        (_, email) = parseaddr(username)
        if not email:
            raise CommandError(f"{email} is not a valid e-mail address.")

        #  Perform the bootstrap

        create_user.apply_async(args=(email, password))
