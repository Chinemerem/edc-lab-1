from ..models import Manifest


class ManifestNotOnDatabase(Exception):
    pass


class ReceiveItem:

    def __init__(self, aliquot=None, manifest=None):
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
