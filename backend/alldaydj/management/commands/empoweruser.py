"""
    AllDay DJ User Empowerment
"""

from alldaydj.tasks import make_superuser
from django.core.management.base import BaseCommand, CommandError, CommandParser
from email.utils import parseaddr
from typing import Any, Optional


class Command(BaseCommand):
    """
    Empowers a user on all or a given tenancy.
    """

    help = "Empowers a user on all or a given tenancy."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("username", type=str)
        parser.add_argument("--staff", action="store_true")
        parser.add_argument("--superuser", action="store_true")
        parser.add_argument("--all", action="store_true")
        parser.add_argument("tenancy", nargs="?", type=str)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:

        username = options["username"]
        staff = options["staff"]
        superuser = options["superuser"]
        all_tenants = options["all"]
        tenancy = options["tenancy"]

        # Sanity checks

        if not username:
            raise CommandError("You must supply a username.")

        (_, email) = parseaddr(username)
        if not email:
            raise CommandError(f"{email} is not a valid e-mail address.")

        if not all_tenants and not tenancy:
            raise CommandError(
                "You must specify all tenancies (--all) or give a specific tenant to assign permissions to."
            )

        #  Perform the bootstrap

        if all_tenants:
            make_superuser.apply_async(args=(username, None, staff, superuser))
        else:
            make_superuser.apply_async(args=(username, tenancy, staff, superuser))
