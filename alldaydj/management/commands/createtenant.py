"""
    AllDay DJ Tenant Creation Command
"""

from alldaydj.tasks import create_tenant
from django.core.management.base import BaseCommand, CommandParser, CommandError
import re
from typing import Any, Optional


class Command(BaseCommand):
    """
    The create tenant command
    """

    help = "Creates a new tenant"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("tenancy", type=str)
        parser.add_argument("owner", type=str)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:

        tenancy = options["tenancy"]
        owner = options["owner"]

        # Sanity checks

        if not re.match("[a-zA-Z]|[a-zA-Z][a-zA-Z0-9]*[a-zA-Z0-9]", tenancy):
            raise CommandError(
                f"{tenancy} is not a valid tenancy name. It must match hostname rules without dashes!"
            )

        if not owner:
            raise CommandError("You must supply a user to own the tenancy.")

        # Create the tenant

        create_tenant.apply_async(args=(tenancy, owner))
