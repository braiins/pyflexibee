import json

class ExchangeRate(object):
    """
    Exchange rate object as required by the flexibee API
    """
    def __init__(self, valid_from, rate, currency='code:UBTC', amount=1000000):
	self.mena = currency
	self.nbStred = rate
	self.platiOdData = valid_from
	self.kurzMnozstvi = amount


class RateRequest(object):
    """
    Represents the exchange rate request
    """
    def __init__(self, rates=[]):
	"""
	@param rates - a list of exchange rates
	"""
	self.rates = rates

    def to_json(self):
	json_dict = {"winstrom":
			 {"@version":"1.0",
			  "kurz": [ r.__dict__ for r in self.rates ]
			  }
		     }

	return json.dumps(json_dict)
