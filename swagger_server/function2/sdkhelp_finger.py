from ctypes import *
from .sdkhelp_base import *
from .HCNetSDK import *


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


def creatFingerCfg(info):
    Cfgs = []
    for f in info["Fingers"]:
        if not f['Valid']:
            continue
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
    dwSize = sizeof(Cfgs[0]) if len(Cfgs) > 0 else 0
    return Cfgs, dwSize


def creatFingerCtrl(info):
    mode = NET_DVR_DEL_FINGER_PRINT_MODE()
    mode.struByCard = NET_DVR_FINGER_PRINT_BYCARD()
    mode.struByCard.byCardNo = (
        c_byte * ACS_CARD_NO_LEN)()
    mode.struByCard.byEnableCardReader = (
        c_byte * MAX_CARD_READER_NUM_512)()
    mode.struByCard.byFingerPrintID = (
        c_byte * MAX_FINGER_PRINT_NUM)()
    mode.struByCard.byRes1 = (c_byte * 34)()
    mode.struByCard.byEnableCardReader[0] = 1
    str_to_bytes(info['CardNo'], mode.struByCard.byCardNo)

    for f in info["Fingers"]:
        i = f['FingerID'] - 1
        v = 1
        #v = 1 if f['Valid'] else 0
        mode.struByCard.byFingerPrintID[i] = v

    ctrl = NET_DVR_FINGER_PRINT_INFO_CTRL()
    ctrl.struProcessMode = mode
    ctrl.byMode = 0
    ctrl.byRes1 = (c_byte * 3)()
    ctrl.byRes = (c_byte * 64)()
    ctrl.dwSize = sizeof(ctrl)
    return ctrl


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


def delFingerData(loginInfo, userinfo):
    param = {'ctrl': NET_DVR_DEL_FINGERPRINT_CFG}
    return sendControl(loginInfo, userinfo, creatFingerCtrl, param)
