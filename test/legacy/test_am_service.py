import unittest
from pyradiodns.radiodns.am_service import RadioDNS_AMService

# this tests backwards compatability with the former 'Service' classes

class TestRadioDNSAMService(unittest.TestCase):

    def setUp(self):
        pass

    def test_it_stores_a_valid_sid(self):
        service = RadioDNS_AMService('drm', 'abcd01')
        self.assertEqual('abcd01', service.sid)

    def test_it_stores_a_valid_type(self):
        service = RadioDNS_AMService('drm', 'abcd01')
        self.assertEqual('drm', service.type)

    def test_it_transforms_an_uppercase_sid(self):
        service = RadioDNS_AMService('drm', 'ABCD01')
        self.assertEqual('abcd01', service.sid)

    def test_it_transforms_an_uppercase_type(self):
        service = RadioDNS_AMService('DRM', 'abcd01')
        self.assertEqual('abcd01', service.sid)

    def test_it_refuses_an_invalid_sid(self):
        with self.assertRaises(ValueError):
            RadioDNS_AMService('drm', 'zzzz01')

    def test_it_refuses_an_invalid_type(self):
        with self.assertRaises(ValueError):
            RadioDNS_AMService('nonsense', 'abcd01')

    def test_it_constructs_an_fqdn(self):
        service = RadioDNS_AMService('amss', 'abcd01')
        self.assertEqual('abcd01.amss.radiodns.org', service.fqdn())

if __name__ == '__main__':
    unittest.main()