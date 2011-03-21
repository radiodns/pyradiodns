Introduction
============

A Python library that facilitates the resolution of an authoritative Fully Qualified Domain Name (FQDN) from the broadcast parameters of an audio service.

From this FQDN it is then possible to discover the advertisement of IP-based applications provided in relation to the queried audio service.

For more information about RadioDNS, please see the official documentation: http://radiodns.org/docs

This is a port of php-radiodns.

Installation
------------

This library depends on dns.resolver, which can be installed from the command line using easy_install dnspython, or by downloading it from http://dnspython.org.

At present, there is no setup.py method of installation.

Usage
-----

There is an example.py included, but simply:

    from pyradiodns.rdns import RadioDNS
    
    rdns = RadioDNS()
    rsp = rdns.lookupDABService('CE1', 'C199', 'C5C9', 0)
    print rsp