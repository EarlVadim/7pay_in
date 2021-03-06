# coding: utf8

session.forget(response)

from time import sleep
#import json
#import datetime
#from decimal import Decimal

import db_common
import crypto_client

def help():
    redirect(URL('index'))

@cache.action(time_expire=300, cache_model=cache.disk) #, vars=False, public=True, lang=True)
def index():
    return dict()

def tx():
    if request.extension == 'html':
        response.view = 'blockchain/res.html'

    txid = request.args(1)
    if not txid:
        return {'error':"need txid: /tx_info.json/[curr]/[txid]"}
    curr_abbrev = request.args(0)
    import db_common
    curr,xcurr,e = db_common.get_currs_by_abbrev(db, curr_abbrev)
    if not xcurr:
        return {"error": "invalid curr:  /tx_info.json/[curr]/[txid]"}
    
    sleep(1)
    conn = crypto_client.conn(curr, xcurr)
    if not conn:
        return {"error": "not connected to wallet"}
    res = None
    try:
        res = conn.getrawtransaction(txid,1) # все выдает
    except Exception as e:
        return { 'error': e }
    
    if 'hex' in res: res.pop('hex')
    txid = res.get('txid')
    if txid: res['txid'] = A(txid, _href=URL('tx',args=[request.args(0), txid]))
    for inp in res.get('vin',[]):
        if 'scriptSig' in inp: inp.pop('scriptSig')
        txid = inp.get('txid')
        if txid:
            inp['txid'] = A(txid, _href=URL('tx',args=[request.args(0), txid]))
        else:
            pass
        pass
    return res
