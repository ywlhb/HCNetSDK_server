from ctypes import *
from .sdkhelp_base import *
from .HCNetSDK import *


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


def creatFaceCfg(info):
    Cfgs = []
    for f in info["Faces"]:
        if not f['Valid']:
            continue
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
    dwSize = sizeof(Cfgs[0]) if len(Cfgs) > 0 else 0
    return Cfgs, dwSize


def creatFaceCtrl(info):
    mode = NET_DVR_DEL_FACE_PARAM_MODE()
    mode.struByCard = NET_DVR_FACE_PARAM_BYCARD()
    mode.struByCard.byCardNo = (
        c_byte * ACS_CARD_NO_LEN)()
    mode.struByCard.byEnableCardReader = (
        c_byte * MAX_CARD_READER_NUM_512)()
    mode.struByCard.byFaceID = (
        c_byte * MAX_FACE_NUM)()
    mode.struByCard.byRes1 = (c_byte * 42)()
    mode.struByCard.byEnableCardReader[0] = 1
    str_to_bytes(info['CardNo'], mode.struByCard.byCardNo)

    for f in info["Faces"]:
        i = f['FaceID'] - 1
        v = 1
        #v = 1 if f['Valid'] else 0
        mode.struByCard.byFaceID[i] = v

    ctrl = NET_DVR_FACE_PARAM_CTRL()
    ctrl.struProcessMode = mode
    ctrl.byMode = 0
    ctrl.byRes1 = (c_byte * 3)()
    ctrl.byRes = (c_byte * 64)()
    ctrl.dwSize = sizeof(ctrl)
    return ctrl

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


def delFaceData(loginInfo, userinfo):
    param = {'ctrl': NET_DVR_DEL_FACE_PARAM_CFG}
    return sendControl(loginInfo, userinfo, creatFaceCtrl, param)
