import time
import datetime
import threading
from ctypes import *
import struct
from .HCNetSDK import *
import copy
import base64


def InitSDK():
    m_bInitSDK = dll.NET_DVR_Init()
    return m_bInitSDK


def Login(Address, UserName, Password, Port):
    struLoginInfo = NET_DVR_USER_LOGIN_INFO()
    struDeviceInfoV40 = NET_DVR_DEVICEINFO_V40()
    struDeviceInfoV40.struDeviceV30 = NET_DVR_DEVICEINFO_V30()
    struDeviceInfoV40.struDeviceV30.sSerialNumber = (c_byte * SERIALNO_LEN)()

    lUserID = -1

    struLoginInfo.sDeviceAddress = bytes(Address, encoding="utf8")
    struLoginInfo.sUserName = bytes(UserName, encoding="utf8")
    struLoginInfo.sPassword = bytes(Password, encoding="utf8")
    struLoginInfo.wPort = Port
    struLoginInfo.bUseAsynLogin = 0

    lUserID = dll.NET_DVR_Login_V40(struLoginInfo, struDeviceInfoV40)
    nErr = dll.NET_DVR_GetLastError()
    return lUserID, nErr


def Login_dict(loginInfo):
    return Login(loginInfo['Address'], loginInfo['UserName'],
                 loginInfo['Password'], loginInfo['Port'])


def Logout(UserID):
    return dll.NET_DVR_Logout(UserID)


_wait_event = threading.Event()
_wait_senf_event = threading.Event()
g_Callback_Data = []
g_Callback_Success = False


def Data_func(lpBuffer, dwBufLen):
    pass


def Status_func(lpBuffer):
    pass

g_Data_func = Data_func
g_Status_func = Status_func


def ProcessCallback(dwType, lpBuffer, dwBufLen, pUserData):
    if pUserData is None:
        return
    global g_Callback_Data, g_Callback_Success
    if dwType == NET_SDK_CALLBACK_TYPE.DATA.value:
        g_Data_func(lpBuffer, dwBufLen)
    elif dwType == NET_SDK_CALLBACK_TYPE.STATUS.value:
        if dwBufLen >= 4:
            buff = cast(lpBuffer, POINTER(c_byte * dwBufLen))
            state = struct.unpack_from('I', buff.contents, 0)[0]
            if state == NET_SDK_CALLBACK_STATUS_NORMAL.SUCCESS.value:
                g_Callback_Success = True
                _wait_event.set()
            elif state == NET_SDK_CALLBACK_STATUS_NORMAL.FAILED.value:
                g_Callback_Success = False
                _wait_event.set()
            elif state == NET_SDK_CALLBACK_STATUS_NORMAL.PROCESSING.value:
                g_Status_func(buff)
            else:
                pass
    else:
        print("Error")
        _wait_event.set()
    _wait_senf_event.set()


g_Callback = fRemoteConfigCallback(ProcessCallback)


def sendData(loginInfo, dataInfo, creatCond, creatSend, param,
             do_Data_f, do_Status_f, do_Return_f):
    UserID, nErr = Login_dict(loginInfo)
    if(UserID < 0):
        return "", UserID

    global g_Data_func, g_Status_func
    g_Data_func = do_Data_f
    g_Status_func = do_Status_f
    g_Callback_Data.clear()
    m_CondHandle = -1
    m_SendHandle = -1
    nErr = 0
    _wait_event.clear()
    condBuff, dwSize = creatCond(dataInfo)
    m_CondHandle = dll.NET_DVR_StartRemoteConfig(
        UserID, param['cond'], pointer(condBuff),
        dwSize, g_Callback, pointer(condBuff))
    if m_CondHandle > -1:
        if 'send' in param.keys():
            sendBuff, dwSize = creatSend(dataInfo)
            if isinstance(sendBuff, list):
                sendBuffs = sendBuff
            else:
                sendBuffs = [sendBuff]
            for sb in sendBuffs:
                _wait_senf_event.clear()
                m_SendHandle = dll.NET_DVR_SendRemoteConfig(
                    m_CondHandle, param['send'], pointer(sb), dwSize)
                if m_SendHandle < 0:
                    nErr = dll.NET_DVR_GetLastError()
                    break
                _wait_senf_event.wait(2)
        _wait_event.wait(5)
        dll.NET_DVR_StopRemoteConfig(m_CondHandle)
    else:
        nErr = dll.NET_DVR_GetLastError()
    Logout(UserID)
    return do_Return_f(m_CondHandle, m_SendHandle, nErr)


def creatCardCond(cardinfo, isone=True):
    setCardCond = NET_DVR_CARD_CFG_COND()
    setCardCond.dwSize = sizeof(setCardCond)
    setCardCond.wLocalControllerID = 0
    setCardCond.dwCardNum = 1 if isone else 0xffffffff
    setCardCond.byCheckCardNo = 1
    dwSize = sizeof(setCardCond)
    return setCardCond, dwSize


def str_to_bytes(strvalue, bs):
    temp = bytes(strvalue, encoding="utf8")
    for index in range(len(temp)):
        bs[index] = temp[index]


def creatSendCard(cardinfo):
    sendCardCfg = NET_DVR_CARD_CFG_SEND_DATA()
    sendCardCfg.byCardNo = (c_byte * ACS_CARD_NO_LEN)()
    sendCardCfg.dwSize = sizeof(sendCardCfg)
    str_to_bytes(cardinfo['CardNo'], sendCardCfg.byCardNo)
    sendCardCfg.dwCardUserId = 0
    dwSize = sizeof(sendCardCfg)
    return sendCardCfg, dwSize


def creatCardCfg(cardinfo):
    setCardCfg = NET_DVR_CARD_CFG_V50()
    setCardCfg.byDoorRight = (c_byte * MAX_DOOR_NUM_256)()
    setCardCfg.byBelongGroup = (c_byte * MAX_GROUP_NUM_128)()
    setCardCfg.wCardRightPlan = (
        c_ushort * MAX_DOOR_NUM_256 * MAX_CARD_RIGHT_PLAN_NUM)()
    setCardCfg.byCardNo = (c_byte * ACS_CARD_NO_LEN)()
    setCardCfg.byCardPassword = (c_byte * CARD_PASSWORD_LEN)()
    setCardCfg.byName = (c_byte * NAME_LEN)()
    setCardCfg.byRes2 = (c_byte * 3)()
    setCardCfg.byLockCode = (c_byte * MAX_LOCK_CODE_LEN)()
    setCardCfg.byRoomCode = (c_byte * MAX_DOOR_CODE_LEN)()
    setCardCfg.byRes3 = (c_byte * 83)()
    setCardCfg.struValid = NET_DVR_VALID_PERIOD_CFG()
    setCardCfg.struValid.struBeginTime = NET_DVR_TIME_EX()
    setCardCfg.struValid.struEndTime = NET_DVR_TIME_EX()
    setCardCfg.dwSize = sizeof(setCardCfg)

    str_to_bytes(cardinfo['CardNo'], setCardCfg.byCardNo)
    setCardCfg.dwModifyParamType = 0
    setCardCfg.dwModifyParamType |= 0x1
    setCardCfg.byCardValid = cardinfo['CardValid']
    setCardCfg.dwModifyParamType |= 0x2
    setCardCfg.struValid.byEnable = 1
    setCardCfg.struValid.struBeginTime.wYear = 2017
    setCardCfg.struValid.struBeginTime.byMonth = 1
    setCardCfg.struValid.struBeginTime.byDay = 1
    setCardCfg.struValid.struBeginTime.byHour = 1
    setCardCfg.struValid.struBeginTime.byMinute = 1
    setCardCfg.struValid.struBeginTime.bySecond = 1
    setCardCfg.struValid.struEndTime.wYear = 2019
    setCardCfg.struValid.struEndTime.byMonth = 1
    setCardCfg.struValid.struEndTime.byDay = 1
    setCardCfg.struValid.struEndTime.byHour = 1
    setCardCfg.struValid.struEndTime.byMinute = 1
    setCardCfg.struValid.struEndTime.bySecond = 1
    setCardCfg.dwModifyParamType |= 0x4
    setCardCfg.byCardType = 1
    setCardCfg.dwModifyParamType |= 0x8
    setCardCfg.byDoorRight[0] = 1
    setCardCfg.dwModifyParamType |= 0x100
    setCardCfg.wCardRightPlan[0][0] = 1
    setCardCfg.dwModifyParamType |= 0x400
    setCardCfg.dwEmployeeNo = int(cardinfo['EmployeeNo'])
    setCardCfg.dwModifyParamType |= 0x800
    str_to_bytes(cardinfo['Name'], setCardCfg.byName)
    setCardCfg.dwCardUserId = int(cardinfo['EmployeeNo'])
    dwSize = sizeof(setCardCfg)
    return setCardCfg, dwSize


def Data_func_setcard(lpBuffer, dwBufLen):
    pass


def Status_func_setcard(lpBuffer):
    cardNob = struct.unpack_from('32s', lpBuffer.contents, 4)[0]
    cardNo = string_at(cardNob).decode(encoding="utf-8", errors="strict")
    g_Callback_Data.append(cardNo)


def Return_func_setcard(condHandle, sendHandle, err):
    if condHandle > -1 and sendHandle > -1:
        return g_Callback_Data, 0
    else:
        return "Error (%s)" % err, -1


def Data_func_getcard(lpBuffer, dwBufLen):
    card_cfg = cast(lpBuffer, POINTER(NET_DVR_CARD_CFG_V50))
    cardNo = string_at(card_cfg.contents.byCardNo).decode(
        encoding="utf-8", errors="strict")
    name = string_at(card_cfg.contents.byName).decode(
        encoding="utf-8", errors="strict")
    rb = {"CardNo": cardNo,
          "EmployeeNo": card_cfg.contents.dwEmployeeNo,
          "Name": name,
          "CardUserId": card_cfg.contents.dwCardUserId}
    g_Callback_Data.append(rb)


def Status_func_getcard(lpBuffer):
    pass


def Return_func_getcard(condHandle, sendHandle, err):
    if condHandle > -1 and sendHandle > -1:
        return g_Callback_Data, 0
    else:
        return "Error (%s)" % err, -1


def creatFingerCond(info):
    Cond = NET_DVR_FINGER_PRINT_INFO_COND()
    Cond.byCardNo = (c_byte * ACS_CARD_NO_LEN)()
    Cond.byEnableCardReader = (c_byte * MAX_CARD_READER_NUM_512)()
    Cond.dwSize = sizeof(Cond)
    Cond.dwFingerPrintNum = len(
        info['Fingers']) if 'Fingers' in info.keys() else 0xffffffff
    Cond.byFingerPrintID = 0xff
    Cond.byCallbackMode = 0
    str_to_bytes(info['CardNo'], Cond.byCardNo)
    Cond.byEnableCardReader[0] = 1
    dwSize = sizeof(Cond)
    return Cond, dwSize


def Data_func_getFinger(lpBuffer, dwBufLen):
    cfg = cast(lpBuffer, POINTER(NET_DVR_FINGER_PRINT_CFG))
    cardNo = string_at(cfg.contents.byCardNo).decode(
        encoding="utf-8", errors="strict")
    data = ""
    if cfg.contents.dwFingerPrintLen > 0:
        bs = cast(cfg.contents.byFingerData,
                  POINTER(c_char * cfg.contents.dwFingerPrintLen))
        data = base64.b64encode(bs.contents).decode(
                    encoding="utf-8", errors="strict")
    rb = {"CardNo": cardNo,
          "FingerPrintID": cfg.contents.byFingerPrintID,
          "FingerPrintData": data}
    g_Callback_Data.append(rb)


def Status_func_getFinger(lpBuffer):
    pass


def Return_func_getFinger(condHandle, sendHandle, err):
    if condHandle > -1:
        return g_Callback_Data, 0
    else:
        return "Error (%s)" % err, -1


def getFingerData(loginInfo, userinfo):
    param = {'cond': NET_DVR_GET_FINGERPRINT_CFG}
    return sendData(loginInfo, userinfo,
                    creatFingerCond, None, param,
                    Data_func_getFinger, Status_func_getFinger,
                    Return_func_getFinger)


def creatFaceCond(info):
    Cond = NET_DVR_FACE_PARAM_COND()
    Cond.byCardNo = (c_byte * ACS_CARD_NO_LEN)()
    Cond.byEnableCardReader = (c_byte * MAX_CARD_READER_NUM_512)()
    Cond.dwSize = sizeof(Cond)
    Cond.dwFaceNum = len(
        info['Faces']) if 'Faces' in info.keys() else 0xffffffff
    Cond.byFaceID = 0xff
    Cond.byFaceDataType = 1
    str_to_bytes(info['CardNo'], Cond.byCardNo)
    Cond.byEnableCardReader[0] = 1
    dwSize = sizeof(Cond)
    return Cond, dwSize


def Data_func_getFace(lpBuffer, dwBufLen):
    cfg = cast(lpBuffer, POINTER(NET_DVR_FACE_PARAM_CFG))
    cardNo = string_at(cfg.contents.byCardNo).decode(
        encoding="utf-8", errors="strict")
    data = ""
    if cfg.contents.dwFaceLen > 0:
        bs = cast(cfg.contents.pFaceBuffer,
                  POINTER(c_char * cfg.contents.dwFaceLen))
        data = base64.b64encode(bs.contents).decode(
            encoding="utf-8", errors="strict")
    rb = {"CardNo": cardNo,
          "FaceID": cfg.contents.byFaceID,
          "FaceData": data}
    g_Callback_Data.append(rb)


def Status_func_getFace(lpBuffer):
    pass


def Return_func_getFace(condHandle, sendHandle, err):
    if condHandle > -1:
        return g_Callback_Data, 0
    else:
        return "Error (%s)" % err, -1


def getFaceData(loginInfo, userinfo):
    param = {'cond': NET_DVR_GET_FACE_PARAM_CFG}
    return sendData(loginInfo, userinfo,
                    creatFaceCond, None, param,
                    Data_func_getFace, Status_func_getFace,
                    Return_func_getFace)


def getCardData(loginInfo, userinfo):
    param = {'cond': NET_DVR_GET_CARD_CFG_V50, 'send': 0x3}
    return sendData(loginInfo, userinfo,
                    creatCardCond, creatSendCard, param,
                    Data_func_getcard, Status_func_getcard,
                    Return_func_getcard)


def getUserData(loginInfo, userinfo):
    re = {"No": userinfo['CardNo']}
    objre, intre = getCardData(loginInfo, userinfo)
    if intre != 0:
        return objre, intre
    re['cards'] = copy.deepcopy(objre)
    objre, intre = getFingerData(loginInfo, userinfo)
    if intre != 0:
        return objre, intre
    re['fingers'] = copy.deepcopy(objre)
    objre, intre = getFaceData(loginInfo, userinfo)
    if intre != 0:
        return objre, intre
    re['faces'] = copy.deepcopy(objre)
    return re, intre


def creatFaceCfg(info):
    Cfgs = []
    for f in info["Faces"]:
        Cfg = NET_DVR_FACE_PARAM_CFG()
        Cfg.byCardNo = (c_byte * ACS_CARD_NO_LEN)()
        Cfg.byEnableCardReader = (c_byte * MAX_CARD_READER_NUM_512)()
        Cfg.byEnableCardReader[0] = 1
        Cfg.byFaceID = f["FaceID"]
        Cfg.byFaceDataType = 1
        Cfg.byRes = (c_byte * 126)()
        Cfg.dwSize = sizeof(Cfg)
        str_to_bytes(info['CardNo'], Cfg.byCardNo)
        bs = base64.b64decode(f["Facedata"])
        Cfg.dwFaceLen = len(bs)
        c_bs = (c_byte * Cfg.dwFaceLen)()
        for index in range(Cfg.dwFaceLen):
            c_bs[index] = bs[index]
        Cfg.pFaceBuffer = cast(c_bs, c_void_p)
        Cfgs.append(Cfg)
    dwSize = sizeof(Cfg)
    return Cfgs, dwSize


def Data_func_setFace(lpBuffer, dwBufLen):
    cfg = cast(lpBuffer, POINTER(NET_DVR_FACE_PARAM_STATUS))
    cardNo = string_at(cfg.contents.byCardNo).decode(
        encoding="utf-8", errors="strict")
    rb = {"CardNo": cardNo,
          "FaceID": cfg.contents.byFaceID,
          "RecvStatus": cfg.contents.byCardReaderRecvStatus[0],
          "TotalStatus": cfg.contents.byTotalStatus,
          "byErrorMsg": string_at(cfg.contents.byErrorMsg).decode(
              encoding="utf-8", errors="strict")}
    print(rb)
    g_Callback_Data.append(rb)


def Status_func_setFace(lpBuffer):
    pass


def Return_func_setFace(condHandle, sendHandle, err):
    if condHandle > -1:
        return g_Callback_Data, 0
    else:
        return "Error (%s)" % err, -1


def setFaceData(loginInfo, userinfo):
    param = {'cond': NET_DVR_SET_FACE_PARAM_CFG, 'send': 0x9}
    return sendData(loginInfo, userinfo,
                    creatFaceCond, creatFaceCfg, param,
                    Data_func_setFace, Status_func_setFace,
                    Return_func_setFace)


def creatFingerCfg(info):
    Cfgs = []
    for f in info["Fingers"]:
        Cfg = NET_DVR_FINGER_PRINT_CFG()
        Cfg.byCardNo = (c_byte * ACS_CARD_NO_LEN)()
        Cfg.byEnableCardReader = (c_byte * MAX_CARD_READER_NUM_512)()
        Cfg.byFingerData = (c_byte * MAX_FINGER_PRINT_LEN)()
        Cfg.byRes1 = (c_byte * 30)()
        Cfg.byRes = (c_byte * 64)()
        Cfg.dwSize = sizeof(Cfg)
        str_to_bytes(info['CardNo'], Cfg.byCardNo)
        Cfg.byFingerPrintID = f["FingerID"]
        Cfg.byFingerType = 0
        Cfg.byEnableCardReader[0] = 1
        bs = base64.b64decode(f["Fingerdata"])
        Cfg.dwFingerPrintLen = len(bs)
        for index in range(Cfg.dwFingerPrintLen):
            Cfg.byFingerData[index] = bs[index]
        Cfgs.append(Cfg)
    dwSize = sizeof(Cfgs[0])
    return Cfgs, dwSize


def Data_func_setFinger(lpBuffer, dwBufLen):
    cfg = cast(lpBuffer, POINTER(NET_DVR_FINGER_PRINT_STATUS))
    cardNo = string_at(cfg.contents.byCardNo).decode(
        encoding="utf-8", errors="strict")
    rb = {"CardNo": cardNo,
          "FingerID": cfg.contents.byFingerPrintID,
          "RecvStatus": cfg.contents.byCardReaderRecvStatus[0],
          "TotalStatus": cfg.contents.byTotalStatus,
          "byErrorMsg": string_at(cfg.contents.byErrorMsg).decode(
              encoding="utf-8", errors="strict")}
    print(rb)
    g_Callback_Data.append(rb)


def Status_func_setFinger(lpBuffer):
    pass


def Return_func_setFinger(condHandle, sendHandle, err):
    if condHandle > -1:
        return g_Callback_Data, 0
    else:
        return "Error (%s)" % err, -1


def setFingerData(loginInfo, userinfo):
    param = {'cond': NET_DVR_SET_FINGERPRINT_CFG, 'send': 0x3}
    return sendData(loginInfo, userinfo,
                    creatFingerCond, creatFingerCfg, param,
                    Data_func_setFinger, Status_func_setFinger,
                    Return_func_setFinger)


def setCardData(loginInfo, userinfo):
    param = {'cond': NET_DVR_SET_CARD_CFG_V50, 'send': 0x3}
    return sendData(loginInfo, userinfo,
                    creatCardCond, creatCardCfg, param,
                    Data_func_setcard, Status_func_setcard,
                    Return_func_setcard)


def setUserData(loginInfo, userinfo):
    re = {"No": userinfo['CardNo']}
    objre, intre = setCardData(loginInfo, userinfo)
    if intre != 0:
        return objre, intre
    else:
        re["CardNum"] = len(objre)
    objre, intre = setFingerData(loginInfo, userinfo)
    if intre != 0:
        return objre, intre
    else:
        re["FingerNum"] = len(objre)
    objre, intre = setFaceData(loginInfo, userinfo)
    if intre != 0:
        return objre, intre
    else:
        re["FaceNum"] = len(objre)
    return "OK %s" % re, intre


def setDatetime(dt: datetime):
    redt = NET_DVR_TIME()
    redt.dwYear = dt.year
    redt.dwMonth = dt.month
    redt.dwDay = dt.day
    redt.dwHour = 0
    redt.dwMinute = 0
    redt.dwSecond = 0
    return redt


def creatEventCond(condinfo):
    eventCond = NET_DVR_ACS_EVENT_COND()
    eventCond.struStartTime = setDatetime(condinfo['StartTime'])
    eventCond.struEndTime = setDatetime(condinfo['EndTime'])
    eventCond.byCardNo = (c_byte * ACS_CARD_NO_LEN)()
    eventCond.byName = (c_byte * NAME_LEN)()
    eventCond.byRes2 = (c_byte * 3)()
    eventCond.byRes = (c_byte * 244)()
    eventCond.dwSize = sizeof(eventCond)
    eventCond.dwMajor = 0x5
    eventCond.dwMinor = 0
    eventCond.byPicEnable = 0
    eventCond.dwBeginSerialNo = condinfo['BeginSerialNo']
    eventCond.dwEndSerialNo = condinfo['EndSerialNo']
    dwSize = sizeof(eventCond)
    return eventCond, dwSize


def Data_func_getevent(lpBuffer, dwBufLen):
    event_cfg = cast(lpBuffer, POINTER(NET_DVR_ACS_EVENT_CFG))
    cardNo = string_at(event_cfg.contents.struAcsEventInfo.byCardNo).decode(
            encoding="utf-8", errors="strict")
    g_Callback_Data.append(
        "No.%s [%s-%s-%s %s:%s:%s] %x-%x cardNo:%s  EmployeeNo:%s  DoorNo:%s  CardType:%s" %
        (event_cfg.contents.struAcsEventInfo.dwSerialNo,
            event_cfg.contents.struTime.dwYear,
            event_cfg.contents.struTime.dwMonth,
            event_cfg.contents.struTime.dwDay,
            event_cfg.contents.struTime.dwHour,
            event_cfg.contents.struTime.dwMinute,
            event_cfg.contents.struTime.dwSecond,
            event_cfg.contents.dwMajor,
            event_cfg.contents.dwMinor,
            cardNo,
            event_cfg.contents.struAcsEventInfo.dwEmployeeNo,
            event_cfg.contents.struAcsEventInfo.dwDoorNo,
            event_cfg.contents.struAcsEventInfo.byCardType))


def Status_func_getevent(lpBuffer):
    pass

def getEventData(loginInfo, condinfo):
    UserID, Err = Login_dict(loginInfo)
    if(UserID < 0):
        return "", UserID

    _wait_event.clear()
    global g_Data_func, g_Status_func
    g_Data_func = Data_func_getevent
    g_Status_func = Status_func_getevent

    g_Callback_Data.clear()
    m_lCondHandle = -1
    nErr = 0

    setCond, dwSize = creatEventCond(condinfo)
    m_lCondHandle = dll.NET_DVR_StartRemoteConfig(
        UserID, NET_DVR_GET_ACS_EVENT, pointer(setCond),
        dwSize, g_Callback, pointer(setCond))
    if m_lCondHandle > -1:
        _wait_event.wait(50)
        dll.NET_DVR_StopRemoteConfig(m_lCondHandle)
    else:
        nErr = dll.NET_DVR_GetLastError()
    Logout(UserID)
    if m_lCondHandle > -1:
        return g_Callback_Data, 0
    else:
        return "Error (%s)" % nErr, -1


