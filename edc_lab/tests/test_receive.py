from django.test import TestCase, tag
from django.utils import timezone
from ..models import Aliquot, Box, BoxType
from ..models import Manifest, ManifestItem
from ..receive import ReceiveAliquot
from ..models import Consignee, Shipper


class TestReceive(TestCase):

    def setUp(self):
        self.shipper = Shipper.objects.create(name='Musanga')
        self.consignee = Consignee.objects.create(name="BHP")
        self.manifest = Manifest.objects.create(
            manifest_identifier='M02ABCDQWERT',
            consignee=self.consignee,
            shipper=self.shipper)
        self.manifest_item = ManifestItem.objects.create(
            manifest=self.manifest,
            identifier='AAAO-QWER-2RRR')
        self.aliquot = Aliquot(
            aliquot_identifier='AAAA-EDDD-AAAA',
            aliquot_datetime=timezone.now(),
            condition='10',
        )
        boxtype = BoxType.objects.create(
            name='Buffy Coat', across=10, down=10, total=100)

        box = Box.objects.create(
            box_identifier='AAAO-QWER-2RRR',
            category='testing',
            box_type=boxtype
        )
        box.boxitem_set.create(identifier='AAAA-EDDD-AAAA',
                               position=1)
        box.save()

#     @tag('1')
#     def test_aliqout_in_manifest_contents(self):
#         ManifestHoldingTable.objects.create(
#             identifier='AAAAA-AAAA')
#         a = AliquotHoldingTable.objects.create(
#             identifier='AAAAA-AAAA')
#         ManifestHoldingTable.objects.create(
#             identifier='AAAAA-BBBB')
#         ManifestHoldingTable.objects.create(
#             identifier='FFPOE-AALL')
#         self.assertEqual(a.identifier,
#                          str(ManifestHoldingTable.objects.all().get(
#                              identifier__exact=a.identifier
#                          )))
#
#     @tag('2')
#     def test_alliquot_list_equal_manifest_list(self):
#         AliquotHoldingTable.objects.create(
#             identifier='AAAAA-AAAA')
#         ManifestHoldingTable.objects.create(
#             identifier='AAAAA-AAAA')
#         self.assertEqual(AliquotHoldingTable.objects.count(),
#                          ManifestHoldingTable.objects.count())
#
#     @tag('3')
#     def test_aliqout_not_in_manifest_contents(self):
#         ManifestHoldingTable.objects.create(
#             identifier='AAAAA-AAAA')
#         a = AliquotHoldingTable.objects.create(
#             identifier='VBEEA-BBSS')
#         ManifestHoldingTable.objects.create(
#             identifier='AAAAA-BBBB')
#         ManifestHoldingTable.objects.create(
#             identifier='FFPOE-AALL')
#         self.assertNotIn(a.identifier,
#                          str(ManifestHoldingTable.objects.all().filter(
#                              identifier=a.identifier
#                          )))

    @tag('9')
    def test_manifest_in_database(self):
        """Assert that a manifest exists on the database
        """
        manifest = Manifest(manifest_identifier='M02ABCDQWERT')
        self.assertFalse(manifest.manifest_on_database)
        ReceiveAliquot(manifest=manifest, aliquot=self.aliquot,
                       manifest_item=self.manifest_item)
        self.assertTrue(manifest.manifest_on_database)

    @tag('9')
    def test_manifest_not_in_database(self):
        """Assert that a manifest is not in the database
        """

        manifest = Manifest(manifest_identifier='M01ZXCVBASDF')
        ReceiveAliquot(manifest=manifest, aliquot=self.aliquot,
                       manifest_item=self.manifest_item)
        self.assertFalse(manifest.manifest_on_database)
