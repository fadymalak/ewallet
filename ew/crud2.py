from sqlalchemy.orm import Session
from typing import Optional
from . import models, schemas
# import models , schemas
import datetime
import time
import random
def generate_unique_id():
    id_part1= str(time.time())
    id_part1 = id_part1.split(".")[0]
    id_part2 = str(random.randint(100,999))
    print(id_part2)
    gen_id = int(id_part1 + id_part2)
    return gen_id

from .schemas import ProcessTypes, Transcation

FIRST_OBJECT = 0

def get_wallet(db:Session,wallet_id:int):
    data= db.query(models.Wallet).filter_by(id=wallet_id).first()
    if data:
        return data
    return False

def create_wallet(db:Session,wallet:schemas.Wallet):
    data = db.query(models.Wallet).filter(models.Wallet.mail== wallet.mail).first()
    if data:
        return False
    data = models.Wallet(**wallet.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def update_wallet_balance(db:Session,wallet_id:Optional[int],amount:int,type:schemas.ProcessTypes):
    wallet = db.query(models.Wallet).filter_by(id=wallet_id).first()
    if not wallet:
        return False
    if type == ProcessTypes.deposit:
        total = "%.3f"%(wallet.balance+amount)
        wallet.balance = float(total)
    else:
        if wallet.balance > amount:
            total = "%.3f"%(wallet.balance-amount)
            wallet.balance = float(total)
        else:
            return False
    db.commit()
    db.refresh(wallet)
    return wallet

def make_transcation(db:Session,transcation:Transcation):
    trans = models.Transcation(**transcation.dict())
    try:
        #update wallet balance & check balance sufficient
        if not update_wallet_balance(db,
                                        wallet_id=trans.wallet_id,
                                            amount=trans.amount,
                                                type=trans.type):
            return False
        db.add(trans)
        db.commit()
        db.refresh(trans)
        
        return trans
    except Exception as e:
        return e

def get_transcation(db:Session,trans_id:Optional[int]=None):
    cur = db.query(models.Transcation).filter_by(id=trans_id).first()
    if cur:
        return cur
    else:
        return False

def delete_transcation(db:Session,transcation_id:Optional[int]=None):
    trans = db.query(models.Transcation).filter_by(id=transcation_id).first()

    #prevent transcation from deleted again
    #prevent refunded transcation from delete
    if trans.is_deleted or trans.reference: 
        return False 
    else:
        update_wallet_balance(db,wallet_id=trans.wallet_id,amount=trans.amount,type=ProcessTypes.deposit)
    
    trans.is_deleted = 1 #mark transcation as delete 
    refund_comment = "Refund Transcation: %s - %s"%(trans.id,trans.comment)
    refund_trans = models.Transcation(
                                amount=trans.amount,
                                    wallet_id=trans.wallet_id,
                                        comment=refund_comment,
                                            type=ProcessTypes.deposit,
                                                reference = trans.id)
    db.add(refund_trans)
    db.commit()
    db.refresh(refund_trans)
    return refund_trans
