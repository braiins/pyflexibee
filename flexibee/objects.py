# -*- coding: utf-8 -*-
#
# Copyright © 2015 Braiins Systems s.r.o. <jan.capek@braiins.cz>
#
# This file is part of PyFlexibee <https://github.com/braiins/pyflexibee/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from decimal import Decimal
import json

class DynamicObject(object):
    """
    Simple dynamic object for decoding JSON based on
    required subset of object attributes.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)


    def get_dict_repr(self):
        """
        @return dictionary representation of a dynamic API object
        """
        return self.__dict__


    def __str__(self):
        return json.dumps(self.get_dict_repr(), sort_keys=True, indent=4)


class DynamicObjectWithJSONId(DynamicObject):
    """
    Extended Dynamic object that has a top level element that is used
    as JSON identification string of the object and is not a regular
    attribute (may contain e.g. dashes)
    """
    def __init__(self, **kwargs):
        super(DynamicObjectWithJSONId, self).__init__(**kwargs)


    def get_dict_repr(self):
        """
        @return dictionary representation of a dynamic API object with
        additional toplevel element required by the API. The toplevel
        element is typically a class parameter
        """
        return { self.json_id:
                 super(DynamicObjectWithJSONId, self).get_dict_repr() }



class InvoiceCashPayment(object):
    """
    This object allows cash invoice payments.
    """
    json_id = 'hotovostni-uhrada'

    def __init__(self, invoice_id, **kwargs):
        self.invoice_id = invoice_id
        self.items = kwargs


    def get_dict_repr(self):
        """
        @return dictionary representation of a dynamic API object with
        additional toplevel element required by the API. The toplevel
        element is typically a class parameter
        """
        return { 'id': self.invoice_id,
                 self.json_id: self.items }



class ExchangeRate(DynamicObject):
    """
    Exchange rate object as required by the flexibee API.
    Also provides conversion services.
    """

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    @classmethod
    def new_for_update(cls, valid_from, rate, currency='code:UBTC',
                       amount=1000000):
        """
        Dedicated method for creating an ExchangeRate instance
        intended for update.
        """
        return cls(mena=currency,
                   nbStred=rate,
                   platiOdData=valid_from,
                   kurzMnozstvi=amount)


    def convert_to_currency(self, value):
        """
        Converts a specified value in base currency to the
        currency for this exchange rate.
        """
        return (Decimal(value) * Decimal(self.kurzMnozstvi) / \
            Decimal(self.nbStred))




class BankTransaction(DynamicObject):
    """
    Bank transaction object is fully dynamic as varying parts of
    transactions are needed for automated processing.
    """
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
