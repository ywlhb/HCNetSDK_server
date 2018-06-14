import time
import datetime
import threading
import struct
import copy
import base64

from ctypes import *
from .HCNetSDK import *


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


def sendControl(loginInfo, dataInfo, creatCtrl, param):
    UserID, nErr = Login_dict(loginInfo)
    if(UserID < 0):
        return "", UserID
    ctrlBuff = creatCtrl(dataInfo)
    m_re = dll.NET_DVR_RemoteControl(UserID,
                                     param['ctrl'],
                                     pointer(ctrlBuff),
                                     sizeof(ctrlBuff))
    nErr = dll.NET_DVR_GetLastError()
    Logout(UserID)
    return m_re, nErr


def str_to_bytes(strvalue, bs):
    temp = bytes(strvalue, encoding="utf8")
    for index in range(len(temp)):
        bs[index] = temp[index]


def str_to_bytes_gbk(strvalue, bs):
    temp = bytes(strvalue, encoding="gbk")
    for index in range(len(temp)):
        bs[index] = temp[index]


def setDatetime(dt: datetime):
    redt = NET_DVR_TIME()
    redt.dwYear = dt.year
    redt.dwMonth = dt.month
    redt.dwDay = dt.day
    redt.dwHour = 0
    redt.dwMinute = 0
    redt.dwSecond = 0
    return redt
