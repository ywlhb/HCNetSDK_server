# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLogController(BaseTestCase):
    """LogController integration test stubs"""

    def test_get_log(self):
        """Test case for get_log

        Read logs from the controller
        """
        query_string = [('actionHandle', 'actionHandle_example'),
                        ('StartTime', '2013-10-20T19:20:30+01:00'),
                        ('EndTime', '2013-10-20T19:20:30+01:00'),
                        ('Major', 56),
                        ('Minor', 56),
                        ('BeginSerialNo', 56),
                        ('End_Serial_Number', 56)]
        response = self.client.open(
            '/v1/Log',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
