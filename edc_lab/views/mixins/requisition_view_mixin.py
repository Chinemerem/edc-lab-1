import re

from edc_constants.constants import UUID_PATTERN


class RequisitionViewMixin:

    @property
    def selected_items(self):
        if not self._selected_items:
            for pk in self.request.POST.getlist(
                    self.form_action_selected_items_name):
                if re.match(UUID_PATTERN, pk):
                    self._selected_items.append(pk)
        return self._selected_items

    @property
    def requisitions(self):
        return self.selected_items
