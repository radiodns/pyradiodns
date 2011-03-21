from service import RadioDNS_Service
import re

class RadioDNS_FMService(RadioDNS_Service):
  
  def __init__(self, country, pi, frequency):    
    # Compile regex patterns
    country_pattern = re.compile('^[0-9A-F]{3}$')
    pi_pattern = re.compile('^[0-9A-F]{4}$')
    
    # Country
    if len(country) == 2:
      self.rds_cc_ecc = None
      this.iso3166_country_code = country
    elif country_pattern.match(country):
      self.rds_cc_ecc = country
      self.iso3166_country_code = None
    else:
      print 'Invalid country value. Must be either a ISO 3166-1 alpha-2 country code or valid hexadecimal value of a RDS Country Code concatanated with a RDS Extended Country Code (ECC).'
      return None
      
    # PI value
    if pi_pattern.match(pi) and (pi[0:1] == self.rds_cc_ecc[0:1] or self.iso3166_country_code == None):
      self.pi = pi
    else:
      print 'Invalid PI value. Must be a valid hexadecimal RDS Programme Identifier (PI) code and the first character must match the first character of the combined RDS Country Code and RDS Extended Country Code (ECC) value (if supplied).'
      return None
    
    # Frequency
    if((isinstance(frequency, float) or isinstance(frequency, int)) and frequency >= 76 and frequency <= 108):
      self.frequency = frequency
    else:
      print 'Invalid frequency value. Must be a valid float between the values 76.0 and 108.0.'
      return None

      
  def toFQDN(self):
    country = self.rds_cc_ecc if self.rds_cc_ecc else self.iso3166_country_code
    fqdn = "%05d.%s.%s.fm.radiodns.org" % (self.frequency * 100, self.pi, country)
    fqdn = fqdn.lower()
    return fqdn
