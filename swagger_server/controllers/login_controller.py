import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.login_info import LoginInfo  # noqa: E501
from swagger_server import util

from swagger_server.function2 import sdk


def login(loginData):  # noqa: E501
    """Login Controler

    Try to login to the controller, such as successful landing, return to the landing handle, all other operations need to use this device handle. # noqa: E501

    :param loginData: Device Login Information
    :type loginData: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        loginData = LoginInfo.from_dict(connexion.request.get_json())  # noqa: E501

    lUserID, nErr = sdk.Login_dict(loginData.to_dict())
    if lUserID >= 0:
        sdk.Logout(lUserID)
        return loginData.to_base64()
    else:
        return "Login Error (%s)" % nErr, 400
