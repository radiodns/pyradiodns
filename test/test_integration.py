import unittest
from pyradiodns.rdns import RadioDNS


class TestService(unittest.TestCase):

    def test_it_actually_works(self):
        rdns = RadioDNS()
        rsp = rdns.lookup_dab('CE1', 'C199', 'C5C9', 0)

        epg = rsp['applications']['radioepg']
        tag = rsp['applications']['radiotag']
        vis = rsp['applications']['radiovis']

        self.assertEqual(False, epg['supported'])
        self.assertEqual(False, tag['supported'])
        self.assertEqual(True, vis['supported'])
        self.assertEqual(
            [{'priority': 0,
            'target': 'srv.foldermedia.com.',
            'weight': 100,
            'port': 80}],
            rsp['applications']['radiovis']['servers'])

if __name__ == '__main__':
    unittest.main()
