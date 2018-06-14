import connexion
import six

# import sys
# sys.path.append('E:/code/Server/HCNetSDK_server/')

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.card import Card  # noqa: E501
from swagger_server.models.finger import Finger  # noqa: E501
from swagger_server.models.face import Face  # noqa: E501
from swagger_server.models.login_info import LoginInfo
from swagger_server import util


from swagger_server.function2 import sdk


def add_user(actionHandle, userData):  # noqa: E501
    """Add a new User to Controler

    Add a new user, add by card number (default to use first card) # noqa: E501

    :param actionHandle: Login Successful Return Action Handle.
    :type actionHandle: str
    :param userData: User Information
    :type userData: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        userData = User.from_dict(connexion.request.get_json())  # noqa: E501
    li = LoginInfo.from_string(actionHandle).to_dict()
    cd = userData.to_cardinfo_dict()
    strRe, intRe = sdk.setUserData(li, cd)
    if intRe == 0:
        return strRe
    else:
        return strRe, 400


def delete_user(actionHandle, CardNos=None, userCodes=None):  # noqa: E501
    """Delete user information from the controller

    Search for the user in the device by card number or user number, and obtain the user&#39;s detailed information. The card number will be used as a priority when providing the card number. # noqa: E501

    :param actionHandle: Login Successful Return Action Handle.
    :type actionHandle: str
    :param CardNos: Card Number
    :type CardNos: List[str]
    :param userCodes: User Number(Employee number)
    :type userCodes: List[int]

    :rtype: int
    """
    if CardNos is None:
        return "", 405
    li = LoginInfo.from_string(actionHandle).to_dict()
    re = []
    for CardNo in CardNos:
        cd = {"CardNo": CardNo, "Fingers": [], "Faces": [],
              "CardValid": False, "EmployeeNo": 1, "Name": ""}
        for i in range(1, 11):
            cd["Fingers"].append({"FingerID": i})
        for i in range(1, 3):
            cd["Faces"].append({"FaceID": i})
        strRe, intRe = sdk.delUserData(li, cd)
        if intRe == 0:
            re.append(strRe)
        else:
            return strRe, 400
    else:
        return "Del OK: %s" % re, 200


def get_user(actionHandle, CardNos=None, userCodes=None):  # noqa: E501
    """Getting user information from the controller

     # noqa: E501

    :param actionHandle: Login Successful Return Action Handle.
    :type actionHandle: str
    :param CardNos: Card Number
    :type CardNos: List[str]
    :param userCodes: User Number(Employee number)
    :type userCodes: List[int]

    :rtype: User
    """
    if CardNos is None:
        return "", 405
    li = LoginInfo.from_string(actionHandle).to_dict()
    re = []
    for CardNo in CardNos:
        cd = {"CardNo": CardNo}
        strRe, intRe = sdk.getUserData(li, cd)
        if intRe == 0:
            u = User(strRe['No'], strRe['Name'])
            ts = str(strRe['EmployeeNo'])
            if len(ts) > 0:
                u.code = ts
            if 'cards' in strRe.keys():
                u.cards = []
                for info in strRe['cards']:
                    u.cards.append(Card(0, info['CardNo']))
            if 'fingers' in strRe.keys():
                u.fingers = []
                for info in strRe['fingers']:
                    u.fingers.append(
                        Finger(info['FingerPrintID'], info['FingerPrintData']))
            if 'faces' in strRe.keys():
                u.faces = []
                for info in strRe['faces']:
                    u.faces.append(
                        Face(info['FaceID'], info['FaceData']))
            re.append(u)
        else:
            return strRe, 400
    else:
        return re, 200


def modify_user(actionHandle, userData):  # noqa: E501
    """Modifying user information in a controller

     # noqa: E501

    :param actionHandle: Login Successful Return Action Handle.
    :type actionHandle: str
    :param userData: User Information
    :type userData: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        userData = User.from_dict(connexion.request.get_json())  # noqa: E501
    li = LoginInfo.from_string(actionHandle).to_dict()
    cd = userData.to_cardinfo_dict()
    strRe, intRe = sdk.delUserData(li, cd)
    strRe, intRe = sdk.setUserData(li, cd)
    if intRe == 0:
        return strRe
    else:
        return strRe, 400
