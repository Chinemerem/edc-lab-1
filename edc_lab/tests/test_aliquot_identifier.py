from django.test import TestCase, tag

from ..identifiers import AliquotIdentifier, Prefix, PrefixKeyError, PrefixLengthError
from ..identifiers import AliquotIdentifierLengthError, AliquotIdentifierCountError


@tag('prefix')
class TestAliquotPrefix(TestCase):

    def test_prefix(self):
        prefix_obj = Prefix(
            template='{opt1}{opt2}',
            length=8,
            opt1='opt1', opt2='opt2')
        self.assertEqual(str(prefix_obj), 'opt1opt2')

    def test_prefix_invalid_length(self):
        self.assertRaises(
            PrefixLengthError,
            Prefix,
            template='{opt1}{opt2}',
            length=7,
            opt1='opt1', opt2='opt2')

    def test_prefix_missing_opt(self):
        self.assertRaises(
            PrefixKeyError,
            Prefix,
            template='{opt1}{opt2}',
            length=8,
            opt1='opt1')


@tag('identifier')
class TestAliquotIdentifier(TestCase):
    def test_valid_length(self):
        AliquotIdentifier(
            identifier_prefix='1234567890',
            numeric_code='22',
            count_padding=2,
            identifier_length=18)

    def test_length_raises(self):
        """Asserts raises exception for invalid identifier length.
        """
        self.assertRaises(
            AliquotIdentifierLengthError,
            AliquotIdentifier,
            identifier_prefix='1234567890',
            count_padding=2,
            identifier_length=0)

    def test_numeric_code(self):
        identifier = AliquotIdentifier(
            identifier_prefix='XXXXXXXX',
            numeric_code='02',
            count_padding=2,
            identifier_length=16)
        self.assertIn('02', str(identifier))

    def test_primary(self):
        identifier = AliquotIdentifier(
            identifier_prefix='XXXXXXXX',
            numeric_code='11',
            count_padding=2,
            identifier_length=16)
        self.assertIn('0000', str(identifier))
        self.assertTrue(identifier.is_primary)

    def test_not_primary_needs_count(self):
        """Asserts need a count if not a primary aliquot.
        """
        self.assertRaises(
            AliquotIdentifierCountError,
            AliquotIdentifier,
            parent_segment='0201',
            identifier_prefix='XXXXXXXX',
            numeric_code='11',
            count_padding=2,
            identifier_length=16)

    def test_not_primary_parent_segment(self):
        identifier = AliquotIdentifier(
            parent_segment='0201',
            identifier_prefix='XXXXXXXX',
            numeric_code='11',
            count=2,
            count_padding=2,
            identifier_length=16)
        self.assertIn('0201', str(identifier))
        self.assertFalse(identifier.is_primary)

    def test_not_primary_parent_segment2(self):
        identifier = AliquotIdentifier(
            parent_segment='0201',
            identifier_prefix='XXXXXXXX',
            numeric_code='11',
            count=2,
            count_padding=2,
            identifier_length=16)
        self.assertIn('1102', str(identifier))
        self.assertFalse(identifier.is_primary)

    def test_large_count_raises_length_error(self):
        self.assertRaises(
            AliquotIdentifierLengthError,
            AliquotIdentifier,
            parent_segment='0201',
            identifier_prefix='XXXXXXXX',
            numeric_code='11',
            count=222,
            count_padding=2,
            identifier_length=16)

    def test_large_count_valid(self):
        try:
            AliquotIdentifier(
                parent_segment='0201',
                identifier_prefix='XXXXXXXX',
                numeric_code='11',
                count=222,
                count_padding=2,
                identifier_length=17)
        except AliquotIdentifierLengthError:
            self.fail('AliquotIdentifierLengthError unexpectedly raised.')
