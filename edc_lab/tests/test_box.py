import re
from django.test import TestCase, tag
from ..models import Box


class TestBox(TestCase):

    box = Box(identifier='2831-9900-8872',
              name='Whole_Blood', category='storage')
    box_2 = None

    @tag('check_box')
    def test_checkBoxIdentifier(self):
        identifier = '2831-9900-8872'
        return self.assertEqual(self.box.identifier, identifier)

    @tag('check_pattern')
    def test_checkIdentifierPattern(self):
        human_readable_pattern = '^[A-Z]{3}\-[0-9]{4}\-[0-9]{2}$'
        return self.assertFalse(
            re.match(human_readable_pattern, self.box.identifier)
        )
