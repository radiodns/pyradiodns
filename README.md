[![Build Status](https://travis-ci.org/radiodns/pyradiodns.png?branch=master)](https://travis-ci.org/radiodns/pyradiodns)

## pyradiodns

`pyradiodns` is a Python library that facilitates the resolution of an authoritative Fully Qualified Domain Name (FQDN) from the broadcast parameters of an audio service.

From this FQDN it is then possible to discover the advertisement of IP-based applications provided in relation to the queried audio service. For more information about RadioDNS, please see the official documentation: http://radiodns.org/docs

This library is essentially a port of php-radiodns.

### Installation

You can install `pyradiodns` using `pip`, like so:

    pip install pyradiodns

### Example Usage

    from pyradiodns.rdns import RadioDNS
    
    rdns = RadioDNS()
    rsp = rdns.lookupDABService('CE1', 'C199', 'C5C9', 0)
    print rsp
