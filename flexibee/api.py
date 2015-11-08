import json
import requests


class Error(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class WinstromRequest(object):
    """
    Base class for all flexibee requests
    """
    json_id = 'winstrom'

    def __init__(self, req_filter=None):
        self.req_filter = req_filter


    def _to_json(self, payload):
	"""
        Helper method that converts the request into JSON

	@param payload_dict - dictionary with the request payload
	@return json formatted request
	"""
	init_payload = {"@version":"1.0" }
	init_payload.update(payload)
	json_dict = { self.__class__.json_id:
                          init_payload
		     }
	return json.dumps(json_dict)


    def get(self, base_url, user, passwd, params={}):
	"""
	Sends the GET request to flexibee.

        @param base_url - base URL path for accessing flexibee
        @param user - username for authentication
        @param password - password for authentication
        @param params - optional query parameters
        @param attributes - optional list of attributes to be fetched
        @return JSON response
	"""
	response = requests.get(self._build_url(base_url), params=params,
				auth=(user, passwd), verify=False)
	return response


    def get_and_build_objects(self, cls, base_url, user, passwd, params={}, 
                              attributes=[]):
	"""
	Sends the GET request to flexibee and builds requested objects
	from the response.

        @param base_url - base URL path for accessing flexibee
        @param cls - class of the object that will be build from the
        JSON response
        @param user - username for authentication
        @param password - password for authentication
        @param params - optional query parameters
        @param attributes - optional list of attributes to be
        fetched. When empty, the object will be build from default
        attributes
        @return a list of objects of a specified class
	"""
        # by default no attributes of the object will be filtered
        # (assume attributes array is empty)
        real_params = {}
        filter_attributes = lambda k: k

        # generate a list of custom details that make flexibee extract
        # only the requested attributes. However, flexibee also
        # provides additional ones like display strings
        # etc.. Therefore, we provide a custom lambda that performs
        # the removal of attributes that were not requested
        if len(attributes) != 0:
            real_params = { 'detail': 'custom:%s' % ','.join(attributes) }
            filter_attributes = lambda k: obj_attrs.pop(k)

        real_params.update(params)
        # fetch the objects
	response = self.get(base_url, user, passwd, real_params)
        response_payload = self._parse_response(response)
        obj_list = []
        # Iterate through all returned JSON objects and build the
        # requested class objects from them. The attributes of the
        # resulting objects will be filtered and only those specified
        # in 'attributes' list will be retained
        for obj_attrs in response_payload[self.__class__.url]:
            # filter only requested attributes
            set(obj_attrs.keys()) - set(attributes)
            # This removes all items from obj_attrs if 'attributes' is
            # non-empty, otherwise it retains the all object
            # attributes
            map(filter_attributes, set(obj_attrs.keys()) - set(attributes))
            obj_list.append(cls(**obj_attrs))

        return obj_list


    def put(self, base_url, user, passwd, params={}):
	"""
	Sends the PUT request to flexibee. The request
	is represented in JSON.
        @param base_url - see put()
        @param user - see put()
        @param password - see put()
        @param params - see put()
        @return JSON response
	"""
	response = requests.put(self._build_url(base_url), params=params,
				data=self._to_json(),
				auth=(user, passwd), verify=False)
	return response


    def _parse_response(self, response):
        """
        Helper method that parses the payload into JSON and returns
        the JSON message payload. If an error is detected, Exception
        is generated.

        @param self - this request instance
        @return - a valid response in JSON format or an exception is
        thrown
        """
        response_json = json.loads(response.content)
        print response_json
        response_top_level = response_json[self.__class__.json_id]
        if response_top_level.has_key('success') and \
                response_top_level['success'].lower() == 'false':
            raise Error("flexibee error: '%s', version: '%s'" %
                        (response_top_level['message'],
                         response_top_level['@version']))
        return response_top_level



    def _build_url(self, base_url):
        """
        Builds full URL for the request

        @param base_url - base URL path for accessing flexibee
        """
        req_filter_str = ''
        if self.req_filter is not None:
            req_filter_str = '/(%s)' % self.req_filter
        url = "%s/%s%s.json" % (base_url, self.__class__.url, req_filter_str)
        return url



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
        super(self.__class__, self).__init__()


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



class BankRequest(WinstromRequest):
    """
    Represents the bank transactions request.
    """
    url = "banka"

    def __init__(self, req_filter=None, transactions=[]):
	"""
	@param transactions - a list of transactions
	"""
	self.transactions = transactions
        super(self.__class__, self).__init__(req_filter)


    def append(self, transaction):
	"""
	Appends a new transaction to the list of transactions
	@param transactions - exchange rate to be appended
	"""
	self.transactions.append(transaction)


    def _to_json(self):
	"""
	Converts the request to json
	"""
	transactions_list = [ t.__dict__ for t in self.transactions ]

	return super(self.__class__, self)._to_json({self.__class__.url : transactions_list})


    def __str__(self):
	return self._to_json()


class PaymentOrderRequest(WinstromRequest):
    """
    Represents the payment order request.
    """
    url = "prikaz-k-uhrade"

    def __init__(self, req_filter=None):
	"""
	@param transactions - a list of transactions
	"""
        super(self.__class__, self).__init__(req_filter)


    def __str__(self):
	return self._to_json()



class DynamicObject(object):
    """
    Simple dynamic object so that we can decode JSON based on
    required subset of object attributes.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)



class ExchangeRate(object):
    """
    Exchange rate object as required by the flexibee API
    """
    def __init__(self, valid_from, rate, currency='code:UBTC', amount=1000000):
	self.mena = currency
	self.nbStred = rate
	self.platiOdData = valid_from
	self.kurzMnozstvi = amount



class BankTransaction(DynamicObject):
    """
    Bank transaction object is fully dynamic as varying parts of
    transactions are needed for automated processing.
    """
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
