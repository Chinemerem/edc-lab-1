from lis.core.lab_reference.models import BaseReferenceList


class GradingList(BaseReferenceList):

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "lab_clinic_reference"
        ordering = ['name']
