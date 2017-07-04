from django.test import TestCase, tag
from ..models import Manifest
from ..receive import ReceiveItem
from ..models import Consignee, Shipper


class TestReceiveItem(TestCase):

    def setUp(self):
        self.shipper = Shipper.objects.create(name='Musanga')
        self.consignee = Consignee.objects.create(name="BHP")
        Manifest.objects.create(manifest_identifier='M02ABCDQWERT',
                                consignee=self.consignee,
                                shipper=self.shipper)

    @tag('1')
    def test_manifest_in_database(self):
        """Assert that a manifest exists on the database
        """
        manifest = Manifest(manifest_identifier='M02ABCDQWERT',
                            consignee=self.consignee,
                            shipper=self.shipper)
        self.assertFalse(manifest.manifest_on_database)
        ReceiveItem(manifest=manifest)
        self.assertTrue(manifest.manifest_on_database)

    @tag('2')
    def test_manifest_not_in_database(self):
        """Assert that a manifest is not in the database
        """
        manifest = Manifest(manifest_identifier='M01ZXCVBASDF',
                            consignee=self.consignee,
                            shipper=self.shipper)
        ReceiveItem(manifest=manifest)
        self.assertFalse(manifest.manifest_on_database)
