# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ValidTime(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, begin_time: datetime=None, end_time: datetime=None, valid: bool=True):  # noqa: E501
        """ValidTime - a model defined in Swagger

        :param begin_time: The begin_time of this ValidTime.  # noqa: E501
        :type begin_time: datetime
        :param end_time: The end_time of this ValidTime.  # noqa: E501
        :type end_time: datetime
        :param valid: The valid of this ValidTime.  # noqa: E501
        :type valid: bool
        """
        self.swagger_types = {
            'begin_time': datetime,
            'end_time': datetime,
            'valid': bool
        }

        self.attribute_map = {
            'begin_time': 'beginTime',
            'end_time': 'endTime',
            'valid': 'valid'
        }

        self._begin_time = begin_time
        self._end_time = end_time
        self._valid = valid

    @classmethod
    def from_dict(cls, dikt) -> 'ValidTime':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ValidTime of this ValidTime.  # noqa: E501
        :rtype: ValidTime
        """
        return util.deserialize_model(dikt, cls)

    @property
    def begin_time(self) -> datetime:
        """Gets the begin_time of this ValidTime.


        :return: The begin_time of this ValidTime.
        :rtype: datetime
        """
        return self._begin_time

    @begin_time.setter
    def begin_time(self, begin_time: datetime):
        """Sets the begin_time of this ValidTime.


        :param begin_time: The begin_time of this ValidTime.
        :type begin_time: datetime
        """

        self._begin_time = begin_time

    @property
    def end_time(self) -> datetime:
        """Gets the end_time of this ValidTime.


        :return: The end_time of this ValidTime.
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: datetime):
        """Sets the end_time of this ValidTime.


        :param end_time: The end_time of this ValidTime.
        :type end_time: datetime
        """

        self._end_time = end_time

    @property
    def valid(self) -> bool:
        """Gets the valid of this ValidTime.

          # noqa: E501

        :return: The valid of this ValidTime.
        :rtype: bool
        """
        return self._valid

    @valid.setter
    def valid(self, valid: bool):
        """Sets the valid of this ValidTime.

          # noqa: E501

        :param valid: The valid of this ValidTime.
        :type valid: bool
        """

        self._valid = valid