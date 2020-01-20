#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import arrow
from bottle import install, request, route, response
from constants import ErrMsg, ErrCode
from globals import g_cfg, g_logger
from external_op import g_ctree_op, g_redis_op, g_db_r, g_db_w
import traceback


@route('/device/importDevices')
def importDevices():
    errcode, data = ErrCode.ErrOK, {}
    return errcode, data

@route('/device/searchByImei')
def searchDeviceByImei():
    errcode, data = ErrCode.ErrOK, {}
    imei = request.params.get('imei', None)
    if imei is None:
        errcode = ErrCode.ErrDataNotFound
        return errcode, data
    dev_info = g_redis_op.getDeviceInfoByImei(imei)
    if dev_info is None or len(dev_info) == 0:
        errcode = ErrCode.ErrDataNotFound
        return errcode, data
    login_id = request.params.get('LOGIN_ID')
    is_ancestor = g_ctree_op.isAncestor(int(login_id), int(dev_info['eid']))
    if not is_ancestor:
        errcode = ErrCode.ErrNoPermission
        return errcode, data
    data = dev_info
    return errcode, data
