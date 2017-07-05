from django.utils import timezone
from django.core.exceptions import ValidationError
from ..models import Aliquot
from ..models import Box, Manifest
from ..models.box_item import BoxItem


class AliquotCountMismatch(Exception):
    pass


class AliquotDoesNotExist(Exception):
    pass


class AliquotDatetimeMismatch(Exception):
    pass


class DuplicateAliquotException(Exception):
    pass


class ManifestNotOnDatabase(Exception):
    pass


class ReceiveAliquot:

    def __init__(self, aliquot=None, manifest_item=None,
                 manifest=None):
        self.aliquot = aliquot
        self.manifest_item = manifest_item
        self.manifest = manifest
        query = None
        try:
            query = Manifest.objects.get(
                manifest_identifier=self.manifest.manifest_identifier)
        except Manifest.DoesNotExist:
            print(
                f'Manifest with identifier={self.manifest.manifest_identifier}'
                ' not on database')

        if query:
            self.manifest.manifest_on_database = True

        if not (self.aliquot.aliquot_datetime <= timezone.now()):
            raise AliquotDatetimeMismatch('some error')
        try:
            box = Box.objects.get(
                box_identifier__exact=manifest_item.identifier)
            temp_aliquot = box.boxitem_set.all().get(
                identifier__exact=aliquot.aliquot_identifier)
            if temp_aliquot:
                self.flag = True
        except BoxItem.DoesNotExist:
            raise BoxItem.DoesNotExist(
                f'Cannot find aliquot: {aliquot.aliquot_identifier}'
                f' in the box items.')

    def __repr__(self):
        return (f'<{self.__class__.__name__}({self.aliquot}, {self.manifest},'
                f'{self.manifest_item})')

    def __str__(self):
        return str(self.aliquot)
