import dns.resolver

class RadioDNS_Service:
  
  dns_resolver = dns.resolver # exists for backwards compatability
  cached_authorative_fqdn = None
  
  def __init__(self):
    pass
    
  def setupDNSResolver(self):
    warnings.warn('this method no longer has any functionality, you can safely remove calls to this method',
                  DeprecationWarning, stacklevel=2)
    
  def resolveAuthorativeFQDN(self):
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
