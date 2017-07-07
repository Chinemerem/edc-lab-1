
from django.test import TestCase, tag
from ..identifiers import Prefix, PrefixMissingLengthError, PrefixLengthError


class TestPrefix(TestCase):

    @tag('prefix_option')
    def test_prefix_missing_option(self):
        self.assertRaises(
            Exception,
            Prefix,
            template='{opt1}{opt2}',
            length=8,
            opt1='opt1')

    @tag('invalid_option')
    def test_prefix_invalid_option(self):
        self.assertRaises(
            Exception,
            Prefix,
            template='{optA}{optB}',
            optA='A',
            optC='B')

    def test_prefix(self):
        prefix_object = Prefix(
            template='{opt1}{opt2}',
            length=8,
            opt1='opt1', opt2='opt2')
        self.assertEqual(str(prefix_object), 'opt1opt2')

    def test_aliquot_prefix_missing_length(self):
        self.assertRaises(
            PrefixMissingLengthError,
            Prefix,
            template='{firstOp}{secondOp}',
            firstOp='first',
            secondOp='second')

    def test_aliquot_prefix_invalid_length(self):
        self.assertRaises(
            PrefixLengthError,
            Prefix,
            template='{opt1}{opt2}{opt3}',
            opt1=45,
            opt2=34,
            opt3=11,
            length=2)
