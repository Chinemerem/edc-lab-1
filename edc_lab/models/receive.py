from django.db import models
from django.utils import timezone


class Receive(models.Model):

    specimen_type = models.CharField(
        max_length=2,
    )
    specimen_condition = models.CharField(
        max_length=2,
        null=True,
        blank=True,
    )

    protocol_number = models.CharField(
        verbose_name='Protocol',
        max_length=15,
        null=True,
        blank=True
    )

    site_code = models.CharField(
        max_length=2,
        null=True,
        blank=True,
    )

    receive_identifier = models.CharField(
        max_length=25,
        editable=False,
        unique=True
    )

    receive_datetime = models.DateTimeField(
        default=timezone.now
    )

    # patient = models.ForeignKey(Patient, null=True, blank=False)

    specimen_reference = models.CharField(
        max_length=25,
        help_text='A unique reference for this patient\'s specimen',
        null=True,
        blank=True,
    )

    collection_datetime = models.DateTimeField()

    clinician_initials = models.CharField(
        verbose_name='Clinician\'s initials',
        max_length=3,
    )

    tube_count = models.IntegerField(default=1, null=True, blank=False)

    # history = AuditTrail()

    def __str__(self):
        return '{}: {}'.format(
            self.receive_identifier,
            self.receive_datetime.strftime('%Y-%m-%d %H:%M'))

    class Meta:
        app_label = 'edc-lab'


"""
    def save(self, *args, **kwargs):
        if not self.id and not self.receive_identifier:
            self.receive_identifier = ReceiveIdentifier().identifier
        if not self.specimen_reference:
            self.specimen_reference = '{}-{}'.format(
                self.collection_datetime.strftime('%Y-%m-%d %H:%M'),
                 self.specimen_type)
        super(Receive, self).save(*args, **kwargs)"""

# db_table = 'getresults_receive'
# unique_together=(('patient', 'collection_datetime', 'specimen_type'), )
