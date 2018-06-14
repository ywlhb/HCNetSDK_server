from ctypes import *
from .sdkhelp_base import *
from .HCNetSDK import *


def creatCardCond(cardinfo, isone=True):
    setCardCond = NET_DVR_CARD_CFG_COND()
    setCardCond.dwSize = sizeof(setCardCond)
    setCardCond.wLocalControllerID = 0
    setCardCond.dwCardNum = 1 if isone else 0xffffffff
    setCardCond.byCheckCardNo = 1
    dwSize = sizeof(setCardCond)
    return setCardCond, dwSize


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
    setCardCfg.struValid.struEndTime.wYear = 2030
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
    str_to_bytes_gbk(cardinfo['Name'], setCardCfg.byName)
    setCardCfg.dwCardUserId = int(cardinfo['EmployeeNo'])
    dwSize = sizeof(setCardCfg)
    return setCardCfg, dwSize


def Data_func_getcard(lpBuffer, dwBufLen):
    card_cfg = cast(lpBuffer, POINTER(NET_DVR_CARD_CFG_V50))
    cardNo = string_at(card_cfg.contents.byCardNo).decode(
        encoding="utf-8", errors="strict")
    name = string_at(card_cfg.contents.byName).decode(
        encoding="GBK", errors="strict")
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


def getCardData(loginInfo, userinfo):
    param = {'cond': NET_DVR_GET_CARD_CFG_V50, 'send': 0x3}
    return sendData(loginInfo, userinfo,
                    creatCardCond, creatSendCard, param,
                    Data_func_getcard, Status_func_getcard,
                    Return_func_getcard)


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


def setCardData(loginInfo, userinfo):
    param = {'cond': NET_DVR_SET_CARD_CFG_V50, 'send': 0x3}
    return sendData(loginInfo, userinfo,
                    creatCardCond, creatCardCfg, param,
                    Data_func_setcard, Status_func_setcard,
                    Return_func_setcard)
