import json
import requests

class WinstromRequest(object):
    """
    Base class for all flexibee requests
    """

    def _to_json(self, payload):
	"""
	@param payload_dict - dictionary with the request payload
	@return json formatted request
	"""
	init_payload = {"@version":"1.0" }
	init_payload.update(payload)
	json_dict = {"winstrom":
			 init_payload
		     }
	return json.dumps(json_dict)


    def send(self, url, user, passwd):
	"""
	Sends the request to flexibee
	"""
	response = requests.put("%s/%s.json" % (url, self.__class__.url),
				data=self._to_json(),
				auth=(user, passwd), verify=False)
	return response


class RateRequest(WinstromRequest):
    """
    Represents the exchange rate request
    """
    url = "kurz"

    def __init__(self, rates=[]):
	"""
	@param rates - a list of exchange rates
	"""
	self.rates = rates


    def append(self, rate):
	"""
	Appends a new rate to the list of exchange rates
	@param rate - exchange rate to be appended
	"""
	self.rates.append(rate)


    def _to_json(self):
	"""
	Converts the request to json
	"""
	rates_list = [ r.__dict__ for r in self.rates ]

	return super(self.__class__, self)._to_json({"kurz" : rates_list})


    def __str__(self):
	return self._to_json()


class ExchangeRate(object):
    """
    Exchange rate object as required by the flexibee API
    """
    def __init__(self, valid_from, rate, currency='code:UBTC', amount=1000000):
	self.mena = currency
	self.nbStred = rate
	self.platiOdData = valid_from
	self.kurzMnozstvi = amount
