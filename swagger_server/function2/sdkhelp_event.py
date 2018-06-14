from ctypes import *
from .sdkhelp_base import *
from .HCNetSDK import *


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


def Return_func_getevent(condHandle, sendHandle, err):
    if condHandle > -1:
        return g_Callback_Data, 0
    else:
        return "Error (%s)" % err, -1


def getEventData(loginInfo, condinfo):
    param = {'cond': NET_DVR_GET_ACS_EVENT}
    return sendData(loginInfo, condinfo,
                    creatEventCond, None, param,
                    Data_func_getevent, Status_func_getevent,
                    Return_func_getevent)
