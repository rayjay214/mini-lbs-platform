#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import arrow
from bottle import install, request, route, response
from constants import ErrMsg, ErrCode
from globals import g_cfg
from globals import g_logger
from businessdb import BusinessDb
import traceback
from ctree_op import CtreeOp
from customer_tree_pb2 import CustomerInfo

@route('/ent/getEntInfoByEid')
def getEntInfoByEid():
    errcode, data = ErrCode.ErrOK, {}
    eid = request.params.get('eid', None)
    if eid is None:
        errcode = ErrCode.ErrLackParam
        return errcode, data
    tree_op = CtreeOp(g_cfg['ctree'])
    customer = tree_op.getCustomInfoByEid(int(eid))
    data['eid'] = customer.eid
    data['pid'] = customer.pid
    data['login_name'] = customer.login_name
    data['phone'] = customer.phone
    g_logger.info(type(customer.addr))
    data['addr'] = customer.addr
    data['email'] = customer.email
    data['leaf'] = customer.is_leaf
    return errcode, data

@route('/ent/getEntChildrenByEid')
def getEntChildrenByEid():
    errcode, data = ErrCode.ErrOK, {}
    eid = request.params.get('eid', None)
    if eid is None:
        errcode = ErrCode.ErrLackParam
        return errcode, data
    records = []
    tree_op = CtreeOp(g_cfg['ctree'])
    customer = tree_op.getCustomInfoByEid(int(eid))
    data['eid'] = customer.eid
    data['pid'] = customer.pid
    data['text'] = '''{}({}/{})'''.format(customer.login_name, customer.own_dev_num, customer.total_dev_num)
    data['phone'] = customer.phone
    data['addr'] = customer.addr
    data['email'] = customer.email
    data['leaf'] = customer.is_leaf
    children, channel = tree_op.getChildrenInfoByEid(int(eid)) #caller have to close channel manually
    for child in children:
        info = {}
        info['eid'] = child.eid
        info['text'] = '''{}({}/{})'''.format(child.login_name, child.own_dev_num, child.total_dev_num)
        info['addr'] = child.addr
        info['phone'] = child.phone
        info['email'] = child.email
        info['leaf'] = child.is_leaf
        records.append(info)

    channel.close()
    data['records'] = records
    return errcode, data

@route('/ent/addEnt')
def addEnt():
    errcode, data = ErrCode.ErrOK, {}
    ent = {}
    ent['pid'] = request.params.get('pid', None)
    ent['login_name'] = request.params.get('login_name', None)
    ent['pwd'] = request.params.get('pwd', None)
    ent['addr'] = request.params.get('addr', '')
    ent['email'] = request.params.get('email', '')
    ent['phone'] = request.params.get('phone', '')
    if None in (ent['pid'], ent['login_name'], ent['pwd']):
        errcode = ErrCode.ErrLackParam
        return errcode, data
    db = BusinessDb(g_cfg['db_business_w'])
    errcode = db.add_ent(ent)
    data['msg'] = ErrMsg[errcode]
    return errcode, data

@route('/ent/deleteEnt')
def deleteEnt():
    errcode, data = ErrCode.ErrOK, {}
    ent = {}
    ent['eid'] = request.params.get('eid', None)
    if ent['eid'] is None:
        errcode = ErrCode.ErrLackParam
        return errcode, data
    db = BusinessDb(g_cfg['db_business_w'])
    errcode = db.delete_ent(ent)
    return errcode, data

@route('/ent/updateEnt')
def updateEnt():
    g_logger.info('enter')
    errcode, data = ErrCode.ErrOK, {}
    eid = request.params.get('eid', None)
    pid = request.params.get('pid', None)
    phone = request.params.get('phone', None)
    addr = request.params.get('addr', None)
    email  = request.params.get('email', None)
    if eid is None:
        g_logger.warn('eid is none')
        errcode = ErrCode.ErrLackParam
        return errcode, data
    db_r = BusinessDb(g_cfg['db_business_r'])
    errcode, ent = db_r.get_ent_by_eid(eid)
    if errcode != ErrCode.ErrOK:
        data['msg'] = ErrMsg[errcode]
        return errcode, data
    ent['pid'] = pid if pid is not None else ent['pid']
    ent['phone'] = phone if phone is not None else ent['phone']
    ent['addr'] = addr if addr is not None else ent['addr']
    ent['email'] = email if email is not None else ent['email']
    db_w = BusinessDb(g_cfg['db_business_w'])
    errcode = db_w.update_ent(ent)
    return errcode, data




