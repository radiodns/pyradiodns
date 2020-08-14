import unittest

from pyradiodns.bearer import AMBearer

class TestRadioDNSAMService(unittest.TestCase):

    def test_it_stores_a_valid_sid(self):
        service = AMBearer('drm', 'abcd01')
        self.assertEqual('abcd01', service.sid)

    def test_it_stores_a_valid_type(self):
        service = AMBearer('drm', 'abcd01')
        self.assertEqual('drm', service.type)

    def test_it_transforms_an_uppercase_sid(self):
        service = AMBearer('drm', 'ABCD01')
        self.assertEqual('abcd01', service.sid)

    def test_it_transforms_an_uppercase_type(self):
        service = AMBearer('DRM', 'abcd01')
        self.assertEqual('abcd01', service.sid)

    def test_it_refuses_an_invalid_sid(self):
        with self.assertRaises(ValueError):
            AMBearer('drm', 'zzzz01')

    def test_it_refuses_an_invalid_type(self):
        with self.assertRaises(ValueError):
            AMBearer('nonsense', 'abcd01')

    def test_it_constructs_an_fqdn(self):
        service = AMBearer('amss', 'abcd01')
        self.assertEqual('abcd01.amss.radiodns.org', service.fqdn())

if __name__ == '__main__':
    unittest.main()
