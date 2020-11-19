"""
    Hacky work-around to ensure the public tenancy is created first.
"""

from alldaydj.tenants.models import Tenant
from alldaydj.users.models import TenantUser
from alldaydj.test.utils import create_public_tenant
from rest_framework.test import APITestCase
from typing import List


class SetupTests(APITestCase):
    """
    Perform the initial setup.
    """

    ADMIN_USERNAME = "admin@example.com"
    ADMIN_PASSWORD = "1337h@x0r"
    PUBLIC_TENANT: Tenant = None

    @classmethod
    def setUpClass(cls):

        # Create the public tenancy and setup the admin user

        create_public_tenant(cls.ADMIN_USERNAME, cls.ADMIN_PASSWORD)
        admin_user = TenantUser.objects.filter(email=cls.ADMIN_USERNAME).first()
        admin_user.set_password(cls.ADMIN_PASSWORD)
        admin_user.save()

        # Give everyone access (we'll need this for setting up other tenancies later)

        cls.PUBLIC_TENANT = Tenant.objects.filter(name="Public Tenant").first()

        super(SetupTests, cls).setUpClass()

    def test_ready_to_go(self):
        """
        Tests we're ready to go with the other tests.
        """

        self.assertIsNotNone(self.PUBLIC_TENANT)
