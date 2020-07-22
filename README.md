[![Build Status](https://travis-ci.org/radiodns/pyradiodns.png?branch=master)](https://travis-ci.org/radiodns/pyradiodns)

## pyradiodns

`pyradiodns` is a Python library that facilitates the resolution of an authoritative Fully Qualified Domain Name (FQDN) from the broadcast parameters of an audio service.

From this FQDN it is then possible to discover the advertisement of IP-based applications provided in relation to the queried audio service. For more information about RadioDNS, please see the official documentation: http://radiodns.org/docs

This library is essentially a port of php-radiodns.

### Installation

Download the entire package, then do

    cd pyradiodns
    sudo python setup.py install
    
which will install pyradiodns to your local packages

### Example Usage

    from pyradiodns.rdns import RadioDNS
    
    rdns = RadioDNS()
    rsp = rdns.lookup_dab('ce1', 'ce15', 'c221', 0)
    print rsp
