'''
Created on Jun 30, 2017

@author: moffat
'''
from django.test import TestCase, tag
from django.utils import timezone
from ..models import Aliquot, Manifest, ManifestItem, Box, BoxType, BoxItem
from ..receive import (
    ReceiveAliquot, AliquotDatetimeMismatch, AliquotDoesNotExist)
from ..models import Consignee, Shipper

import datetime


class TestAliquotReceived(TestCase):

    def setUp(self):
        self.shipper = Shipper.objects.create(name='Musanga')
        self.consignee = Consignee.objects.create(name="BHP")
        self.manifest = Manifest.objects.create(
            manifest_identifier='M02ABCDQWERT',
            consignee=self.consignee,
            shipper=self.shipper)

    @tag('a')
    def test_received_aliquot_date_not_infuture(self):
        """Test if the received aliquot date is
        not in the future
        """
        aliquot = Aliquot(
            aliquot_identifier='AAAA-EDDD-AAAA',
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
        manifest_item = ManifestItem.objects.create(
            manifest=self.manifest,
            identifier='AAAO-QWER-2RRR')
        ReceiveAliquot(aliquot=aliquot,
                       manifest_item=manifest_item, manifest=self.manifest)
        self.assertTrue(aliquot.aliquot_datetime <= timezone.now())

    @tag('b')
    def test_received_aliquot_date_infuture(self):
        aliquot = Aliquot(
            aliquot_identifier='AAAA-EDDD-AAAA',
            aliquot_datetime=timezone.now() + datetime.timedelta(days=10),
            condition='10',
        )
        boxtype = BoxType.objects.create(
            name='Buffy Coat', across=10, down=10, total=100)

        box = Box.objects.create(
            box_identifier='AAAA-EDDD-AAAA',
            category='testing',
            box_type=boxtype
        )
        box.boxitem_set.create(identifier='AAAA-EDDD-AAAA',
                               position=1)
        box.save()
        manifest_item = ManifestItem.objects.create(
            manifest=self.manifest,
            identifier='AAAO-QWER-2RRR')

        self.assertRaises(
            AliquotDatetimeMismatch,
            ReceiveAliquot,
            aliquot=aliquot,
            manifest_item=manifest_item,
            manifest=self.manifest)

    @tag('c')
    def test_received_valid_aliquot(self):

        boxtype = BoxType.objects.create(
            name='Buffy Coat', across=10, down=10, total=100)

        box = Box.objects.create(
            box_identifier='2831-9900-8872',
            category='testing',
            box_type=boxtype
        )
        box.boxitem_set.create(identifier='AAAA-EDDD-AAAA',
                               position=1)
        box.save()
        aliquot = Aliquot(
            aliquot_identifier='AAAA-EDDD-AAAA',
        )
        manifest_item = ManifestItem.objects.create(
            identifier='2831-9900-8872',
            manifest=self.manifest)
        receive = ReceiveAliquot(aliquot=aliquot,
                                 manifest_item=manifest_item,
                                 manifest=self.manifest)
        self.assertTrue(receive.flag)

    @tag('d')
    def test_received_invalid_aliquot(self):
        """Assert raises an exception if the aliquot
        received does not appear in the manifest items
        """
        boxtype = BoxType.objects.create(
            name='Buffy Coat', across=10, down=10, total=100)

        box = Box.objects.create(
            box_identifier='2831-9900-8872',
            category='testing',
            box_type=boxtype
        )
        box.boxitem_set.create(identifier='AAAA-EDDD-AAAA',
                               position=1)
        box.boxitem_set.create(identifier='AAAA-EDDD-CCCC',
                               position=2)
        box.save()

        aliquot = Aliquot(
            aliquot_identifier='AAAA-OOOO-AAAA',
        )
        manifest_item = ManifestItem.objects.create(
            manifest=self.manifest,
            #             manifest_id=1,
            identifier='2831-9900-8872')

        try:
            ReceiveAliquot(
                aliquot=aliquot,
                manifest_item=manifest_item, manifest=self.manifest)
        except BoxItem.DoesNotExist:
            self.assertRaisesMessage(
                BoxItem.DoesNotExist,
                f'cannot find the aliquot {aliquot.aliquot_identifier}')
