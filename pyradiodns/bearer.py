import re

import dns.resolver

class Bearer:
  
  dns_resolver = dns.resolver # exists for backwards compatibility only
  cached_authorative_fqdn = None
  
  def __init__(self):
    pass
    
  def setupDNSResolver(self): # exists for backwards compatibility only
    warnings.warn('this method no longer has any functionality, you can safely remove calls to this method',
                  DeprecationWarning, stacklevel=2)

  def resolve_authorative_fqdn(self):
    try:
      r = dns.resolver.resolve(self.fqdn(), 'CNAME')
    except AttributeError:
      r = dns.resolver.query(self.fqdn(), 'CNAME')
    if not r:
      return False
    if len(r) == 0:
      return False
    self.cached_authorative_fqdn = r[0].target.to_text()
    return self.cached_authorative_fqdn
    
  def resolveAuthorativeFQDN(self): # exists for backwards compatibility only
    return self.resolve_authorative_fqdn()
    
  def resolve(self, application_id, transport_protocol='TCP'):
    if self.cached_authorative_fqdn:
      authorative_fqdn = self.cached_authorative_fqdn
    else:
      authorative_fqdn = self.resolveAuthorativeFQDN()
    if not authorative_fqdn:
      return False
    application_fqdn = "_%s._%s.%s" % (application_id.lower(), transport_protocol.lower(), authorative_fqdn)
    try:
      try:
        r = dns.resolver.resolve(application_fqdn, 'SRV')
      except AttributeError:
        r = dns.resolver.query(application_fqdn, 'SRV')
      if len(r) == 0:
        return False
      results = []
      for answer in r:
        results.append({
          'target': answer.target.to_text(),
          'port': answer.port,
          'priority': answer.priority,
          'weight': answer.weight,
        })
      return results
    except dns.resolver.NXDOMAIN:
      # Non-existent domain
      return False
    except dns.resolver.NoAnswer:
      # no authoritive answer
      return False

class AMBearer(Bearer):
  
  def __init__(self, type, sid):
    type = type.lower()
    if type == 'drm' or type == 'amss':
      self.type = type
    else:
      raise ValueError("Type value must be either 'drm' or 'amss'")
    
    if re.compile('^[0-9A-Fa-f]{6}$').match(sid):
      self.sid = sid.lower()
    else:
      raise ValueError('Service Identifier (SId) must be a valid 6-character hexadecimal.');
      
  def fqdn(self):
    fqdn = "%s.%s.radiodns.org" % (self.sid, self.type)
    return fqdn.lower()

class DABBearer(Bearer):
  
  def __init__(self, ecc, eid, sid, scids, data=None):
    # Compile regex patterns
    ecc_pattern = re.compile('^[0-9A-Fa-f]{3}$')
    eid_pattern = re.compile('^[0-9A-Fa-f]{4}$')
    sid_pattern = re.compile('^[0-9A-Fa-f]{4}$|^[0-9A-Fa-f]{8}$')
    scids_pattern = re.compile('^[0-9A-Fa-f]{1}$|^[0-9A-Fa-f]{3}$')
    data_pattern = re.compile('^[0-9A-Fa-f]{2}-[0-9A-Fa-f]{3}$')
    
    # ECC
    if ecc_pattern.match(ecc):
      self.ecc = ecc
    else:
      print('Invalid Global Country Code (GCC) value. Must be a valid 3-character hexadecimal.');
      return None
      
    # EID
    if eid_pattern.match(eid):
      self.eid = eid
    else:
      print('Invalid Ensembled Identifier (EId) value. Must be a valid 4-character hexadecimal.');
      return None
      
    # SID
    if sid_pattern.match(sid):
      self.sid = sid
    else:
      print('Invalid Service Identifier (SId) value. Must be a valid 4 or 8-character hexadecimal.');
      return None
      
    # SCIDS
    if scids_pattern.match(str(scids)):
      self.scids = scids
    else:
      print('Invalid Service Component Identifer within the Service (SCIdS) value. Must be a valid 3-character hexadecimal.');
      return None
      
    # AppTy/UAtype
    if data:
      self.data = data
      if xpad_pattern.match(data):
        self.xpad = self.data
        self.pa = None
      elif isinstance(data, int) and 0 >= self.data <= 1023:
        self.xpad = None
        self.pa = self.data
      else:
        print('Invalid data value. Must be either a valid X-PAD Applicaton Type (AppTy) and User Application type (UAtype) hexadecimal or Packet Address integer.')
        return None
    else:
      self.data = None  
      
      
  def fqdn(self):
    fqdn = "%s.%s.%s.%s.dab.radiodns.org" % (self.scids, self.sid, self.eid, self.ecc)
    if self.data:
      if self.xpad:
        fqdn = sprintf('%s.%s', self.xpad, fqdn)
      elif self.pa:
        fqdn = sprintf('%s.%s', self.pa, fqdn)
    fqdn = fqdn.lower()
    return fqdn

class FMBearer(Bearer):

    def __init__(self, country, pi, frequency):
        country_pattern = re.compile('^[0-9A-Fa-f]{3}$')
        pi_pattern = re.compile('^[0-9A-Fa-f]{4}$')

        # Country
        if country_pattern.match(country):
            self.country = country
        else:
            raise ValueError('Invalid GCC code')

        # TODO Tidy this up
        # Must be a valid hexadecimal RDS Programme Identifier (PI) code
        # and the first character must match the first character of the
        # combined RDS Country Code and RDS Extended Country Code (ECC)
        # value (if supplied).
        if pi_pattern.match(pi):
            self.pi = pi
        else:
            raise ValueError('Invalid PI value')
            
        if self.country[0] != self.pi[0]:
            raise ValueError('GCC and PI code should start with the same character')

        if isinstance(frequency, float) or isinstance(frequency, int):
            if frequency > 108:
                raise ValueError('Frequency can not be above 108.0 Mhz')
            elif frequency < 76:
                raise ValueError('Frequency can not be below 76.0 Mhz')
            self.frequency = frequency
        else:
            raise ValueError('Frequency must be a number')

    def fqdn(self):
        fqdn = "%05d.%s.%s.fm.radiodns.org" %\
            (self.frequency * 100, self.pi, self.country)
        return fqdn.lower()

class HDBearer(Bearer):
  
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
    fqdn = "%s.%s.hd.radiodns.org" % (self.tx, self.cc) 
    if self.mid != None:
        fqdn = ("%s." % (self.mid)) + fqdn
    
    return fqdn.lower()
