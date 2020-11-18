"""
    Joins an AllDay DJ user to a tenancy.
"""

from alldaydj.tasks import join_user_tenancy
from django.core.management.base import BaseCommand, CommandError, CommandParser
from typing import Any, Optional


class Command(BaseCommand):
    """
    CJoins an AllDay DJ user to a tenancy.
    """

    help = "Joins an AllDay DJ user to a tenancy."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("username", type=str)
        parser.add_argument("tenancy", type=str)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:

        username = options["username"]
        tenancy = options["tenancy"]

        # Sanity checks

        if not username or not tenancy:
            raise CommandError("You must supply a username and tenant name.")

        #  Perform the bootstrap

        join_user_tenancy.apply_async(args=(username, tenancy))
