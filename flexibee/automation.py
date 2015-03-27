# -*- coding: utf-8 -*-
#
import re

class EntryProcessor(object):
    """
    Helper class that provides the accounting operation on string
    match.
    """
    def __init__(self, regexp, op):
        self.regexp = re.compile(regexp)
        self._op = op


    def match(self, str):
        """
        Match string with the processor regexp

        @param self - this processor instance
        @param str - string to be matched
        @return Match instance
        """
        m = self.regexp.match(str)
        return m


    def get_op(self):
        """
        Provides the operation string

        @param self - this processor instance
        @return formatted operation code
        """
        return u'code:%s' % self._op


    @classmethod
    def create_from_tupples(cls, tupples):
        """
        Helper class method that builds processors from tupples
        """
        # materialize all processors
        return map(lambda x: cls(x[0], x[1]), tupples)
