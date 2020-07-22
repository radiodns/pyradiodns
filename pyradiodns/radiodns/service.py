import dns.resolver

class RadioDNS_Service:
  
  dns_resolver = None
  cached_authorative_fqdn = None
  
  def __init__(self):
    pass
    
  def setupDNSResolver(self):
    self.dns_resolver = dns.resolver
    
  def resolveAuthorativeFQDN(self):
    if not self.dns_resolver:
      self.setupDNSResolver()
    r = self.dns_resolver.query(self.fqdn(), 'CNAME')
    if not r:
      return False
    if len(r) == 0:
      return False
    self.cached_authorative_fqdn = r[0].target
    return self.cached_authorative_fqdn
    
  def resolve(self, application_id, transport_protocol='TCP'):
    if self.cached_authorative_fqdn:
      authorative_fqdn = self.cached_authorative_fqdn
    else:
      authorative_fqdn = self.resolveAuthorativeFQDN()
    if not authorative_fqdn:
      return False
    application_fqdn = "_%s._%s.%s" % (application_id.lower(), transport_protocol.lower(), authorative_fqdn)
    if not self.dns_resolver:
      self.setupDNSResolver()
    try:
      r = self.dns_resolver.query(application_fqdn, 'SRV')
      if len(r) == 0:
        return False
      results = []
      for answer in r:
        results.append({
          'target': answer.target,
          'port': answer.port,
          'priority': answer.priority,
          'weight': answer.weight,
        })
      return results
    except dns.resolver.NXDOMAIN:
      # Non-existent domain
      return False
