import unittest
from pyradiodns.radiodns.fm_service import RadioDNS_FMService

# this tests backwards compatability with the former 'Service' classes

class TestRadioDNSFMService(unittest.TestCase):

    def test_it_recognises_an_rds_cc_ecc(self):
        service = RadioDNS_FMService('ce1', 'c0c0', 107)
        self.assertEqual('ce1', service.country)
    
    def test_it_accepts_frequency_as_integer(self):
        service = RadioDNS_FMService('ce1', 'c0c0', 107)
        self.assertEqual(107.0, service.frequency)
    
    def test_it_stores_a_valid_frequency(self):
        service = RadioDNS_FMService('ce1', 'c0c0', 104.9)
        self.assertEqual(104.9, service.frequency)
    
    def test_it_rejects_high_frequencies(self):
        with self.assertRaises(ValueError):
            RadioDNS_FMService('ce1', 'c0c0', 109)
    
    def test_it_rejects_low_frequencies(self):
        with self.assertRaises(ValueError):
            RadioDNS_FMService('ce1', 'c0c0', 60)

    def test_it_rejects_non_numerical_frequencies(self):
        with self.assertRaises(ValueError):
            RadioDNS_FMService('ce1', 'c0c0', 'foo')

    def test_it_constructs_an_fqdn(self):
        service = RadioDNS_FMService('ce1', 'c0c0', 107)
        self.assertEqual('10700.c0c0.ce1.fm.radiodns.org', service.fqdn())

if __name__ == '__main__':
    unittest.main()
