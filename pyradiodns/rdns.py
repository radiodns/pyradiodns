from radiodns.am_service import RadioDNS_AMService
from radiodns.dab_service import RadioDNS_DABService
from radiodns.fm_service import RadioDNS_FMService
from radiodns.hd_service import RadioDNS_HDService

class RadioDNS:
  
  KNOWN_APPLICATIONS = [
    ('radioepg', 'TCP'),
    ('radiotag', 'TCP'),
    ('radiovis', 'TCP'),
  ]
  
  def lookupAMService(self, type=None, sid=None):
    service = RadioDNS_AMService(type, sid)
    return self.lookupService(service)
  
  def lookupDABService(self, ecc=None, eid=None, sid=None, scids=None, data=None):
    service = RadioDNS_DABService(ecc, eid, sid, scids, data);
    return self.lookupService(service)
    
  def lookupFMService(self, country=None, pi=None, frequency=None):
    service = RadioDNS_FMService(country, pi, frequency)
    return self.lookupService(service)
  
  def lookupHDService(self, tx=None, cc=None):
    service = RadioDNS_HDService(tx, cc);
    return self.lookupService(service)
    
  def lookupService(self, service):
    results = {}
    results['authorative_fqdn'] = service.resolveAuthorativeFQDN()
    if not (results['authorative_fqdn']):
      return False
    results['applications'] = {}
    for application in self.KNOWN_APPLICATIONS:
      (application_id, transport) = application
      application_result = service.resolveApplication(application_id, transport)
      results['applications'][application_id] = {}
      results['applications'][application_id]['supported'] = application_result
      if (application_result):
        results['applications'][application_id]['servers'] = application_result
    return results