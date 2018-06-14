# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_add_user(self):
        """Test case for add_user

        Add a new User to Controler
        """
        userData = User()
        query_string = [('actionHandle', 'actionHandle_example')]
        response = self.client.open(
            '/v1/User',
            method='POST',
            data=json.dumps(userData),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_user(self):
        """Test case for delete_user

        Delete user information from the controller
        """
        query_string = [('actionHandle', 'actionHandle_example'),
                        ('CardNos', 'CardNos_example'),
                        ('userCodes', 56)]
        response = self.client.open(
            '/v1/User',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user(self):
        """Test case for get_user

        Getting user information from the controller
        """
        query_string = [('actionHandle', 'actionHandle_example'),
                        ('CardNos', 'CardNos_example'),
                        ('userCodes', 56)]
        response = self.client.open(
            '/v1/User',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_modify_user(self):
        """Test case for modify_user

        Modifying user information in a controller
        """
        userData = User()
        query_string = [('actionHandle', 'actionHandle_example')]
        response = self.client.open(
            '/v1/User',
            method='PUT',
            data=json.dumps(userData),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
