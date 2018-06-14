import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.login_info import LoginInfo
from swagger_server import util
from swagger_server.function2 import sdk

def get_log(actionHandle, StartTime, EndTime, Major=None, Minor=None, BeginSerialNo=None, EndSerialNo=None):  # noqa: E501
    """Read logs from the controller

    Query the device log with the time period, event type, and event sequence number to return the corresponding log information. # noqa: E501

    :param actionHandle: Login Successful Return Action Handle.
    :type actionHandle: str
    :param StartTime: Start time
    :type StartTime: str
    :param EndTime: End Time
    :type EndTime: str
    :param Major: Event main Type
    :type Major: int
    :param Minor: Event Secondary Type
    :type Minor: List[int]
    :param BeginSerialNo: Start serial number
    :type BeginSerialNo: int
    :param End_Serial_Number: 
    :type End_Serial_Number: int

    :rtype: List[str]
    """
    StartTime = util.deserialize_datetime(StartTime)
    EndTime = util.deserialize_datetime(EndTime)
    li = LoginInfo.from_string(actionHandle).to_dict()

    cd = {}
    cd['StartTime'] = StartTime
    cd['EndTime'] = EndTime
    cd['Major'] = Major if Major is not None else 0
    cd['Minor'] = Major if Minor is not None else 0
    cd['BeginSerialNo'] = BeginSerialNo if BeginSerialNo is not None else 0
    cd['EndSerialNo'] = EndSerialNo if EndSerialNo is not None else 0
        
    Re, intRe = sdk.getEventData(li, cd)
    if intRe == 0:
        return Re
    else:
        return Re, 400
