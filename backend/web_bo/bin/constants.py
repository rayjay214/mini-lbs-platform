from enum import IntEnum

class ErrCode(IntEnum):
    ErrOK = 0
    ErrDataNotFound = 1
    ErrLackParam = 2
    ErrPwdNotMatch = 3
    ErrTokenTimeout = 4
    ErrTokenInvalid = 5
    ErrMysqlError = 6
    ErrNoPermission = 7
    ErrEntHasDevice = 8
    ErrEntHasChildren = 9
    ErrTypeNotSupported = 10
    ErrParamInvalid = 11
    ErrPermissionSetInvalid = 12

ErrMsg = {
    0  : 'OK',
    1  : 'data not found',
    2  : 'lack parameter',
    3  : 'pwd not match',
    4  : 'token timeout',
    5  : 'token invalid',
    6  : 'mysql error',
    7  : 'no permission',
    8  : 'account still has devices',
    9  : 'account still has children accounts',
    10 : 'product type not supported',
    11 : 'param invalid',
    12 : 'child could not have greater permission than parent'
}

RedisKeyPrefix = {
    'DeviceInfo' : 'device',
    'Imei' : 'imei',
    'DeviceRunInfo' : 'devruninfo'
}