import sys
import os
from enum import Enum, unique
from ctypes import *
import platform


print(os.getcwd() +  '/swagger_server/linux_dll')
sysstr = platform.system()
print(sysstr)
if sysstr =="Windows" :
    os.environ['path'] += os.getcwd() + '\\swagger_server\\dll;'
    dll = windll.LoadLibrary('..\\dll\\HCNetSDK.dll')
else:
    dll = CDLL(os.getcwd() +  '/swagger_server/linux_dll/libhcnetsdk.so')

NET_DVR_DEV_ADDRESS_MAX_LEN = 129  # device address max length
NET_DVR_LOGIN_USERNAME_MAX_LEN = 64
NET_DVR_LOGIN_PASSWD_MAX_LEN = 64
LOG_INFO_LEN = 11840
MACADDR_LEN = 6

ACS_CARD_NO_LEN = 32
MAX_DOOR_NUM_256 = 256
MAX_CARD_READER_NUM_512 = 512
MAX_FINGER_PRINT_LEN = 768
MAX_FINGER_PRINT_NUM = 10
MAX_FACE_NUM = 2
ERROR_MSG_LEN = 32
CARD_PASSWORD_LEN = 8
MAX_CARD_RIGHT_PLAN_NUM = 4
NAME_LEN = 32
MAX_LOCK_CODE_LEN = 8
MAX_DOOR_CODE_LEN = 8
MAX_GROUP_NUM_128 = 128
ERROR_MSG_LEN = 32
MAX_NAMELEN = 16

SERIALNO_LEN = 48

XML_ABILITY_OUT_LEN = 3 * 1024 * 1024

DEVICE_ABILITY_INFO = 0x011
ACS_ABILITY = 0x801
ALARMHOST_ABILITY = 0x500

NET_DVR_GET_CARD_CFG_V50 = 2178
NET_DVR_SET_CARD_CFG_V50 = 2179
NET_DVR_GET_FINGERPRINT_CFG = 2150
NET_DVR_SET_FINGERPRINT_CFG = 2151
NET_DVR_DEL_FINGERPRINT_CFG = 2152
NET_DVR_GET_CARD_PASSWD_CFG = 2161
NET_DVR_SET_CARD_PASSWD_CFG = 2162
NET_DVR_GET_FACE_PARAM_CFG = 2507
NET_DVR_SET_FACE_PARAM_CFG = 2508
NET_DVR_DEL_FACE_PARAM_CFG = 2509
NET_DVR_GET_ACS_EVENT = 2514

ENUM_ACS_SEND_DATA = 0x3
ENUM_ACS_INTELLIGENT_IDENTITY_DATA = 0x9


class NET_SDK_CALLBACK_TYPE(Enum):
    STATUS = 0
    PROGRESS = 1
    DATA = 2


class NET_SDK_CALLBACK_STATUS_NORMAL(Enum):
    SUCCESS = 1000
    PROCESSING = 1001
    FAILED = 1002
    EXCEPTION = 1003
    LANGUAGE_MISMATCH = 1004
    DEV_TYPE_MISMATCH = 1005
    SEND_WAIT = 1006


class NET_DVR_DEVICEINFO_V30t(Structure):
    _fields_ = [('sSerialNumber', c_byte * SERIALNO_LEN)]


class NET_DVR_DEVICEINFO_V30(Structure):
    _fields_ = [('sSerialNumber', c_byte * SERIALNO_LEN),
                ('byAlarmInPortNum', c_byte),
                ('byAlarmOutPortNum', c_byte),
                ('byDiskNum', c_byte),
                ('byDVRType', c_byte),
                ('byChanNum', c_byte),
                ('byStartChan', c_byte),
                ('byAudioChanNum', c_byte),
                ('byIPChanNum', c_byte),
                ('byZeroChanNum', c_byte),
                ('byMainProto', c_byte),
                ('bySubProto', c_byte),
                ('bySupport', c_byte),
                ('bySupport1', c_byte),
                ('bySupport2', c_byte),
                ('wDevType', c_ushort),
                ('bySupport3', c_byte),
                ('byMultiStreamProto', c_byte),
                ('byStartDChan', c_byte),
                ('byStartDTalkChan', c_byte),
                ('byHighDChanNum', c_byte),
                ('bySupport4', c_byte),
                ('byLanguageType', c_byte),
                ('byVoiceInChanNum', c_byte),
                ('byStartVoiceInChanNo', c_byte),
                ('byRes3', c_byte * 2),
                ('byMirrorChanNum', c_byte),
                ('byMirrorChanNum', c_ushort),
                ('byRes2', c_byte * 2)]


functype = CFUNCTYPE(c_void_p, c_int, c_uint,
                     POINTER(NET_DVR_DEVICEINFO_V30), c_void_p)


class NET_DVR_USER_LOGIN_INFO(Structure):
    _fields_ = [('sDeviceAddress', c_char * NET_DVR_DEV_ADDRESS_MAX_LEN),
                ('byRes1', c_byte),
                ('wPort', c_ushort),
                ('sUserName', c_char * NET_DVR_LOGIN_USERNAME_MAX_LEN),
                ('sPassword', c_char * NET_DVR_LOGIN_PASSWD_MAX_LEN),
                ('cbLoginResult', functype),
                ('pUser', c_void_p),
                ('bUseAsynLogin', c_bool),
                ('byRes2 ', c_byte * 128)]


class NET_DVR_DEVICEINFO_V40(Structure):
    _fields_ = [('struDeviceV30', NET_DVR_DEVICEINFO_V30),
                ('bySupportLock', c_byte),
                ('byRetryLoginTime', c_byte),
                ('byPasswordLevel', c_byte),
                ('byProxyType', c_byte),
                ('dwSurplusLockTime', c_uint),
                ('byCharEncodeType', c_byte),
                ('bySupportDev5', c_byte),
                ('byRes2 ', c_byte * 254)]


class NET_DVR_SDKSTATE(Structure):
    _fields_ = [('dwTotalLoginNum', c_uint),
                ('dwTotalRealPlayNum', c_uint),
                ('dwTotalPlayBackNum', c_uint),
                ('dwTotalAlarmChanNum', c_uint),
                ('dwTotalFormatNum', c_uint),
                ('dwTotalFileSearchNum', c_uint),
                ('dwTotalLogSearchNum', c_uint),
                ('dwTotalSerialNum', c_uint),
                ('dwTotalUpgradeNum', c_uint),
                ('dwTotalVoiceComNum', c_uint),
                ('dwTotalBroadCastNum', c_uint),
                ('dwRes', c_uint * 10)]


class NET_DVR_CARD_CFG_COND(Structure):
    _fields_ = [('dwSize', c_uint),
                ('dwCardNum', c_uint),
                ('byCheckCardNo', c_byte),
                ('byRes1', c_byte * 3),
                ('wLocalControllerID', c_ushort),
                ('byRes2', c_byte * 2),
                ('dwLockID', c_ushort),
                ('byRes3', c_byte * 20)]


class NET_DVR_CARD_CFG_SEND_DATA(Structure):
    _fields_ = [('dwSize', c_uint),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('dwCardUserId', c_uint),
                ('byRes', c_byte * 12)]


class NET_DVR_TIME_EX(Structure):
    _fields_ = [('wYear', c_ushort),
                ('byMonth', c_byte),
                ('byDay', c_byte),
                ('byHour', c_byte),
                ('byMinute', c_byte),
                ('bySecond', c_byte),
                ('byRes', c_byte)]


class NET_DVR_VALID_PERIOD_CFG(Structure):
    _fields_ = [('byEnable', c_byte),
                ('byBeginTimeFlag', c_byte),
                ('byEnableTimeFlag', c_byte),
                ('byTimeDurationNo', c_byte),
                ('struBeginTime', NET_DVR_TIME_EX),
                ('struEndTime', NET_DVR_TIME_EX),
                ('byRes2', c_byte * 32)]


class NET_DVR_CARD_CFG_V50(Structure):
    _fields_ = [('dwSize', c_uint),
                ('dwModifyParamType', c_uint),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('byCardValid', c_byte),
                ('byCardType', c_byte),
                ('byLeaderCard', c_byte),
                ('byRes1', c_byte),
                ('byDoorRight', c_byte * MAX_DOOR_NUM_256),
                ('struValid', NET_DVR_VALID_PERIOD_CFG),
                ('byBelongGroup', c_byte * MAX_GROUP_NUM_128),
                ('byCardPassword', c_byte * CARD_PASSWORD_LEN),
                ('wCardRightPlan', c_ushort *
                 MAX_DOOR_NUM_256 * MAX_CARD_RIGHT_PLAN_NUM),
                ('dwMaxSwipeTime', c_uint),
                ('dwSwipeTime', c_uint),
                ('wRoomNumber', c_ushort),
                ('wFloorNumber', c_ushort),
                ('dwEmployeeNo', c_uint),
                ('byName', c_byte * NAME_LEN),
                ('wDepartmentNo', c_ushort),
                ('wSchedulePlanNo', c_ushort),
                ('bySchedulePlanType', c_byte),
                ('byRes2', c_byte * 3),
                ('dwLockID', c_uint),
                ('byLockCode', c_byte * MAX_LOCK_CODE_LEN),
                ('byRoomCode', c_byte * MAX_DOOR_CODE_LEN),
                ('dwCardRight', c_uint),
                ('dwPlanTemplate', c_uint),
                ('dwCardUserId', c_uint),
                ('byCardModelType', c_byte),
                ('byRes3', c_byte * 83)]


class NET_DVR_CARD_CFG_COND(Structure):
    _fields_ = [('dwSize', c_uint),
                ('dwCardNum', c_uint),
                ('byCheckCardNo', c_byte),
                ('byRes1', c_byte * 3),
                ('wLocalControllerID', c_ushort),
                ('byRes2', c_byte * 2),
                ('dwLockID', c_ushort),
                ('byRes3', c_byte * 20)]


class NET_DVR_CARD_PASSWD_CFG(Structure):
    _fields_ = [('dwSize', c_uint),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('byCardPassword', c_byte * CARD_PASSWORD_LEN),
                ('dwErrorCode', c_uint),
                ('byCardValid', c_byte),
                ('byRes3', c_byte * 23)]


class NET_DVR_FINGER_PRINT_INFO_COND(Structure):
    _fields_ = [('dwSize', c_uint),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('byEnableCardReader', c_byte * MAX_CARD_READER_NUM_512),
                ('dwFingerPrintNum', c_uint),
                ('byFingerPrintID', c_byte),
                ('byCallbackMode', c_byte),
                ('byRes1', c_byte * 26)]


class NET_DVR_FINGER_PRINT_CFG(Structure):
    _fields_ = [('dwSize', c_uint),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('dwFingerPrintLen', c_uint),
                ('byEnableCardReader', c_byte * MAX_CARD_READER_NUM_512),
                ('byFingerPrintID', c_byte),
                ('byFingerType', c_byte),
                ('byRes1', c_byte * 30),
                ('byFingerData', c_byte * MAX_FINGER_PRINT_LEN),
                ('byRes', c_byte * 64)]


class NET_DVR_FINGER_PRINT_STATUS(Structure):
    _fields_ = [('dwSize', c_uint),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('byCardReaderRecvStatus', c_byte * MAX_CARD_READER_NUM_512),
                ('byFingerPrintID', c_byte),
                ('byFingerType', c_byte),
                ('byTotalStatus', c_byte),
                ('byRes1', c_byte),
                ('byErrorMsg', c_byte * ERROR_MSG_LEN),
                ('dwCardReaderNo', c_uint),
                ('byRes', c_byte * 24)]


class NET_DVR_FINGER_PRINT_BYCARD(Structure):
    _fields_ = [('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('byEnableCardReader', c_byte * MAX_CARD_READER_NUM_512),
                ('byFingerPrintID', c_byte * MAX_FINGER_PRINT_NUM),
                ('byRes1', c_byte * 34)]


class NET_DVR_FINGER_PRINT_BYREADER(Structure):
    _fields_ = [('dwCardReaderNo', c_uint),
                ('byClearAllCard', c_byte),
                ('byRes1', c_byte * 3),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('byRes', c_byte * 548)]


class NET_DVR_DEL_FINGER_PRINT_MODE(Union):
    _fields_ = [('uLen', c_byte * 588),
                ('struByCard', NET_DVR_FINGER_PRINT_BYCARD),
                ('struByReader', NET_DVR_FINGER_PRINT_BYREADER)]


class NET_DVR_FINGER_PRINT_INFO_CTRL(Structure):
    _fields_ = [('dwSize', c_uint),
                ('byMode', c_byte),
                ('byRes1', c_byte * 3),
                ('struProcessMode', NET_DVR_DEL_FINGER_PRINT_MODE),
                ('byRes', c_byte * 64)]


class NET_DVR_FACE_PARAM_COND(Structure):
    _fields_ = [('dwSize', c_uint),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('byEnableCardReader', c_byte * MAX_CARD_READER_NUM_512),
                ('dwFaceNum', c_uint),
                ('byFaceID', c_byte),
                ('byFaceDataType', c_byte),
                ('byRes', c_byte * 126)]


class NET_DVR_FACE_PARAM_CFG(Structure):
    _fields_ = [('dwSize', c_uint),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('dwFaceLen', c_uint),
                ('pFaceBuffer', c_void_p),
                ('byEnableCardReader', c_byte * MAX_CARD_READER_NUM_512),
                ('byFaceID', c_byte),
                ('byFaceDataType', c_byte),
                ('byRes', c_byte * 126)]


class NET_DVR_FACE_PARAM_STATUS(Structure):
    _fields_ = [('dwSize', c_uint),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('byCardReaderRecvStatus', c_byte * MAX_CARD_READER_NUM_512),
                ('byErrorMsg', c_byte * ERROR_MSG_LEN),
                ('dwCardReaderNo', c_uint),
                ('byTotalStatus', c_byte),
                ('byFaceID', c_byte),
                ('byRes', c_byte * 130)]


class NET_DVR_FACE_PARAM_BYCARD(Structure):
    _fields_ = [('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('byEnableCardReader', c_byte * MAX_CARD_READER_NUM_512),
                ('byFaceID', c_byte * MAX_FACE_NUM),
                ('byRes1', c_byte * 42)]


class NET_DVR_FACE_PARAM_BYREADER(Structure):
    _fields_ = [('dwCardReaderNo', c_uint),
                ('byClearAllCard', c_byte),
                ('byRes1', c_byte * 3),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('byRes', c_byte * 548)]


class NET_DVR_DEL_FACE_PARAM_MODE(Union):
    _fields_ = [('uLen', c_byte * 588),
                ('struByCard', NET_DVR_FACE_PARAM_BYCARD),
                ('struByReader', NET_DVR_FACE_PARAM_BYREADER)]


class NET_DVR_FACE_PARAM_CTRL(Structure):
    _fields_ = [('dwSize', c_uint),
                ('byMode', c_byte),
                ('byRes1', c_byte * 3),
                ('struProcessMode', NET_DVR_DEL_FACE_PARAM_MODE),
                ('byRes', c_byte * 64)]


class NET_DVR_TIME(Structure):
    _fields_ = [('dwYear', c_uint),
                ('dwMonth', c_uint),
                ('dwDay', c_uint),
                ('dwHour', c_uint),
                ('dwMinute', c_uint),
                ('dwSecond', c_uint)]


class NET_DVR_IPADDR(Structure):
    _fields_ = [('sIpV4', c_byte * 16),
                ('sIpV6', c_byte * 128)]


class NET_DVR_LOG_V30(Structure):
    _fields_ = [('strLogTime', NET_DVR_TIME),
                ('dwMajorType', c_uint),
                ('dwMinorType', c_uint),
                ('sPanelUser', c_byte * NAME_LEN),
                ('sNetUser', c_byte * NAME_LEN),
                ('struRemoteHostAddr', NET_DVR_IPADDR),
                ('dwParaType', c_uint),
                ('dwChannel', c_uint),
                ('dwDiskNumber', c_uint),
                ('dwAlarmInPort', c_uint),
                ('dwAlarmOutPort', c_uint),
                ('dwInfoLen', c_uint),
                ('sInfo', c_byte * LOG_INFO_LEN)]


class NET_DVR_ACS_EVENT_COND(Structure):
    _fields_ = [('dwSize', c_uint),
                ('dwMajor', c_uint),
                ('dwMinor', c_uint),
                ('struStartTime', NET_DVR_TIME),
                ('struEndTime', NET_DVR_TIME),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('byName', c_byte * NAME_LEN),
                ('byPicEnable', c_byte),
                ('byRes2', c_byte * 3),
                ('dwBeginSerialNo', c_uint),
                ('dwEndSerialNo', c_uint),
                ('byRes', c_byte * 244)]


class NET_DVR_ACS_EVENT_DETAIL(Structure):
    _fields_ = [('dwSize', c_uint),
                ('byCardNo', c_byte * ACS_CARD_NO_LEN),
                ('byCardType', c_byte),
                ('byWhiteListNo', c_byte),
                ('byReportChannel', c_byte),
                ('byCardReaderKind', c_byte),
                ('dwCardReaderNo', c_uint),
                ('dwDoorNo', c_uint),
                ('dwVerifyNo', c_uint),
                ('dwAlarmInNo', c_uint),
                ('dwAlarmOutNo', c_uint),
                ('dwCaseSensorNo', c_uint),
                ('dwRs485No', c_uint),
                ('dwMultiCardGroupNo', c_uint),
                ('wAccessChannel', c_ushort),
                ('byDeviceNo', c_byte),
                ('byDistractControlNo', c_byte),
                ('dwEmployeeNo', c_uint),
                ('wLocalControllerID', c_ushort),
                ('byInternetAccess', c_byte),
                ('byType', c_byte),
                ('byMACAddr', c_byte * MACADDR_LEN),
                ('bySwipeCardType', c_byte),
                ('byRes2', c_byte),
                ('dwSerialNo', c_uint),
                ('byChannelControllerID', c_byte),
                ('byChannelControllerLampID', c_byte),
                ('byChannelControllerIRAdaptorID', c_byte),
                ('byChannelControllerIREmitterID', c_byte),
                ('byRes', c_byte * 108)]


class NET_DVR_ACS_EVENT_CFG(Structure):
    _fields_ = [('dwSize', c_uint),
                ('dwMajor', c_uint),
                ('dwMinor', c_uint),
                ('struTime', NET_DVR_TIME),
                ('sNetUser', c_byte * MAX_NAMELEN),
                ('struRemoteHostAddr', NET_DVR_IPADDR),
                ('struAcsEventInfo', NET_DVR_ACS_EVENT_DETAIL),
                ('dwPicDataLen', c_uint),
                ('pPicData', c_void_p),
                ('byRes', c_byte * 64)]


fRemoteConfigCallback = CFUNCTYPE(c_void_p, c_uint, c_void_p,
                                  c_uint, c_void_p)


#21 NET_DVR_FindDVRLog_V30
dll.NET_DVR_FindDVRLog_V30.argtypes = [c_int, c_int, c_int, c_int,
                                       POINTER(NET_DVR_TIME),
                                       POINTER(NET_DVR_TIME),
                                       c_bool]
dll.NET_DVR_FindDVRLog_V30.restype = c_int

#22 NET_DVR_FindNextLog_V30
dll.NET_DVR_FindNextLog_V30.argtypes = [c_int, POINTER(NET_DVR_LOG_V30)]
dll.NET_DVR_FindNextLog_V30.restype = c_int

#23 NET_DVR_FindLogClose_V30
dll.NET_DVR_FindLogClose_V30.argtypes = [c_int]
dll.NET_DVR_FindLogClose_V30.restype = c_bool

#1 NET_DVR_Init
dll.NET_DVR_Init.restype = c_bool

#2 NET_DVR_Login_V40
dll.NET_DVR_Login_V40.argtypes = [POINTER(NET_DVR_USER_LOGIN_INFO),
                                  POINTER(NET_DVR_DEVICEINFO_V40)]
dll.NET_DVR_Login_V40.restype = c_int

#2.2 NET_DVR_Logout
dll.NET_DVR_Logout.argtypes = [c_int]
dll.NET_DVR_Logout.restype = c_bool

#3 NET_DVR_GetLastError
dll.NET_DVR_GetLastError.restype = c_int

#4 NET_DVR_GetSDKVersion
dll.NET_DVR_GetSDKVersion.restype = c_int

#5 NET_DVR_GetSDKBuildVersion
dll.NET_DVR_GetSDKBuildVersion.restype = c_int

#6 NET_DVR_GetSDKState
dll.NET_DVR_GetSDKState.restype = c_bool
dll.NET_DVR_GetSDKState.argtypes = [POINTER(NET_DVR_SDKSTATE)]

#7 NET_DVR_GetDeviceAbility
dll.NET_DVR_GetDeviceAbility.restype = c_bool
dll.NET_DVR_GetDeviceAbility.argtypes = [
    c_int, c_uint, c_char_p, c_uint, c_char_p, c_uint]

#8 NET_DVR_StartRemoteConfig
dll.NET_DVR_StartRemoteConfig.restype = c_int
dll.NET_DVR_StartRemoteConfig.argtypes = [
    c_int, c_uint, c_void_p, c_uint, fRemoteConfigCallback, c_void_p]

#9 NET_DVR_SendRemoteConfig
dll.NET_DVR_SendRemoteConfig.restype = c_bool
dll.NET_DVR_SendRemoteConfig.argtypes = [c_int, c_uint, c_void_p, c_uint]

#10 NET_DVR_StopRemoteConfig
dll.NET_DVR_StopRemoteConfig.restype = c_bool
dll.NET_DVR_StopRemoteConfig.argtypes = [c_int]

#11 NET_DVR_GetRemoteConfigState
dll.NET_DVR_GetRemoteConfigState.restype = c_bool
dll.NET_DVR_GetRemoteConfigState.argtypes = [c_int, c_void_p]

#11 NET_DVR_RemoteControl
dll.NET_DVR_RemoteControl.restype = c_bool
dll.NET_DVR_RemoteControl.argtypes = [c_int, c_uint, c_void_p, c_uint]
