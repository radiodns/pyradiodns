from pyradiodns.bearer import AMBearer, DABBearer, FMBearer, HDBearer

class RadioDNS:

    KNOWN_APPLICATIONS = [
        ('radioepg', 'TCP'),
        ('radiospi', 'TCP'),
        ('radiotag', 'TCP'),
        ('radiovis', 'TCP'),
    ]

    def lookup_am(self, type=None, sid=None):
        service = AMBearer(type, sid)
        return self.__lookup(service)

    def lookup_dab(self, ecc=None, eid=None, sid=None, scids=None, data=None):
        service = DABBearer(ecc, eid, sid, scids, data)
        return self.__lookup(service)

    def lookup_fm(self, country=None, pi=None, frequency=None):
        service = FMBearer(country, pi, frequency)
        return self.__lookup(service)

    def lookup_hd(self, cc=None, tx=None, mid=None):
        service = HDBearer(cc, tx, mid)
        return self.__lookup(service)

    def __lookup(self, service):
        results = {}
        results['authorative_fqdn'] = service.resolveAuthorativeFQDN()
        if not (results['authorative_fqdn']):
            return False
        results['applications'] = {}
        for application in self.KNOWN_APPLICATIONS:
            (app_id, transport) = application
            result = service.resolve(app_id, transport)
            results['applications'][app_id] = {}
            supported = True if result != False else False
            results['applications'][app_id]['supported'] = supported
            if (result):
                results['applications'][app_id]['servers'] = result
        return results
