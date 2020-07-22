from service import RadioDNS_Service
import re

class RadioDNS_HDService(RadioDNS_Service):
  
  def __init__(self, cc, tx, mid):
    # Compile regex patterns
    cc_pattern = re.compile('^[0-9]{3}$')
    tx_pattern = re.compile('^[0-9]{5}$')
    mid_pattern = re.compile('[0-9]{1}')
    
    # Country Check
    if cc_pattern.match(cc):
      self.cc = cc
    else:
      raise ValueError('Invalid Country Value. Must be 3 decimal characters.');
      
    # Facility ID check
    if tx_pattern.match(tx):
      self.tx = tx
    else:
      raise ValueError('Invalid Facility Value. Must be 5 decimal characters.');
    
    # Multicast ID
    if mid == None or mid_pattern.match(mid):
      self.mid = mid
    else:
      raise ValueError('Invalid Multicast Value. Must be 1 decimal character.');
      
  def fqdn(self):
    fqdn = "%s.%s.hd.adiodns.org" % (self.tx, self.cc) 
    if self.mid != None:
        fqdn = ("%s." % (self.mid)) + fqdn
    
    return fqdn.lower()