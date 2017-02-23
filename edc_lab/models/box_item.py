import re

from django.db import models
from django.db.models.deletion import PROTECT

from edc_base.model.models import BaseUuidModel
from edc_dashboard.model_mixins import SearchSlugModelMixin, SearchSlugManager

from .aliquot import pattern as aliquot_identifier_pattern
from .box import Box


class BoxItemManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, position, identifier, box_identifier):
        return self.get(
            position=position,
            identifier=identifier,
            box_identifier=box_identifier)


class BoxItem(SearchSlugModelMixin, BaseUuidModel):

    box = models.ForeignKey(Box, on_delete=PROTECT)

    position = models.IntegerField(null=True)

    identifier = models.CharField(
        max_length=25,
        null=True)

    comment = models.CharField(
        max_length=25,
        null=True,
        blank=True)

    objects = BoxItemManager()

    def natural_key(self):
        return (self.position, self.identifier) + self.box.natural_key()

    @property
    def human_readable_identifier(self):
        """Returns a human readable identifier.
        """
        x = self.identifier
        if re.match(aliquot_identifier_pattern, self.identifier):
            return '{}-{}-{}-{}-{}'.format(x[0:3], x[3:6], x[6:10], x[10:14], x[14:18])
        return self.identifier

    def get_slugs(self):
        slugs = [self.identifier,
                 self.human_readable_identifier]
        return slugs

    class Meta:
        app_label = 'edc_lab'
        ordering = ('position', )
        unique_together = (('box', 'position'), ('box', 'identifier'))