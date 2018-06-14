import copy
from . import sdkhelp_base
from . import sdkhelp_card
from . import sdkhelp_finger
from . import sdkhelp_face
from . import sdkhelp_event


def InitSDK():
    return sdkhelp_base.InitSDK()


def Login(Address, UserName, Password, Port):
    return sdkhelp_base.Login(Address, UserName, Password, Port)


def Login_dict(loginInfo):
    return sdkhelp_base.Login_dict(loginInfo)


def Logout(UserID):
    return sdkhelp_base.Logout(UserID)


def getUserData(loginInfo, userinfo):
    re = {"No": userinfo['CardNo']}
    objre, intre = sdkhelp_card.getCardData(loginInfo, userinfo)
    if intre != 0:
        return objre, intre
    re['cards'] = copy.deepcopy(objre)
    if len(re['cards']):
        re["EmployeeNo"] = re['cards'][0]["EmployeeNo"]
        re["Name"] = re['cards'][0]["Name"]
        re["CardUserId"] = re['cards'][0]["CardUserId"]
    objre, intre = sdkhelp_finger.getFingerData(loginInfo, userinfo)
    if intre != 0:
        return objre, intre
    re['fingers'] = copy.deepcopy(objre)
    objre, intre = sdkhelp_face.getFaceData(loginInfo, userinfo)
    if intre != 0:
        return objre, intre
    re['faces'] = copy.deepcopy(objre)
    return re, intre


def setUserData(loginInfo, userinfo):
    re = {"No": userinfo['CardNo']}
    objre, intre = sdkhelp_card.setCardData(loginInfo, userinfo)
    if intre != 0:
        return objre, intre
    else:
        re["CardNum"] = len(objre)
    objre, intre = sdkhelp_finger.setFingerData(loginInfo, userinfo)
    if intre != 0:
        return objre, intre
    else:
        re["FingerNum"] = len(objre)
    objre, intre = sdkhelp_face.setFaceData(loginInfo, userinfo)
    if intre != 0:
        return objre, intre
    else:
        re["FaceNum"] = len(objre)
    return "OK %s" % re, intre


def delUserData(loginInfo, userinfo):
    re = {"No": userinfo['CardNo']}
    bre, intre = sdkhelp_finger.delFingerData(loginInfo, userinfo)
    re["Finger"] = bre
    if not bre:
        re["FingerErr"] = intre
        return re, -1
    bre, intre = sdkhelp_face.delFaceData(loginInfo, userinfo)
    re["Face"] = bre
    if not bre:
        re["FaceErr"] = intre
        return re, -1
    objre, intre = sdkhelp_card.setCardData(loginInfo, userinfo)
    if intre != 0:
        re["FaceErr"] = objre
        return re, -1
    else:
        re["Card"] = len(objre)
    return re, 0


def getEventData(loginInfo, condinfo):
    return sdkhelp_event.getEventData(loginInfo, condinfo)
