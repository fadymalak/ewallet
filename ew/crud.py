from models import Wallet
from schemas import ProcessTypes
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

FIRST_OBJECT = 0
def get_wallet(exec,wallet_id:int):
    data = exec.execute_statement("SELECT  * from wallet WHERE id =?",wallet_id)
    if data :
        return data
    return False

def create_wallet(exec,wallet:Wallet):
    data = exec.execute_statement("SELECT * FROM wallet Where mail = ?",wallet.mail)
    if data:
        return False
    return exec.execute_statement("INSERT INTO Wallet ?",wallet)
    
def update_wallet_balance(exec,wallet_id,amount,type):
    wallets = exec.execute_statement("SELECT * FROM Wallet WHERE id = ?",wallet_id)
    balance = wallets[FIRST_OBJECT]["balance"]
    if type == ProcessTypes.deposit:
        total = float("%.3f"%(balance+amount))
        cur = exec.execute_statement("UPDATE Wallet set balance =  ?  WHERE id = ?",total,wallet_id)
        data =cur[FIRST_OBJECT]
        return data 
    else:
        if balance > amount :
            total = float("%.3f"%(balance-amount))
            cur = exec.execute_statement("UPDATE Wallet  set balance =  ?  WHERE id = ?",(total),wallet_id)
            data =cur[FIRST_OBJECT]
            return data
        else:
            return False


def make_transcation(exec,transcation):
    data= transcation.dict()
    print(data)
    try:
        cur  = exec.execute_statement("INSERT INTO Transcation ?",data)
        update_wallet_balance(exec,wallet_id=transcation.wallet_id,
                                amount = transcation.amount,
                                    type= transcation.type)
        data =cur[FIRST_OBJECT]
        return data
    except:
        return False

def delete_transcation(exec,transcation_id):
    data = exec.execute_statement("SELECT wallet_id , amount ,comment FROM Transcation Where id = ? AND is_deleted = 0 AND reference = 0",transcation_id)
    if not data:
        return False
    wallet_id = data["wallet_id"]
    amount = data["amount"]
    comment = data["comment"]
    refund_comment = "Refund Transcation: %s - %s"(transcation_id,comment)
    refund_data = {"wallet_id":wallet_id,
                        "amount":amount,
                            "type":ProcessTypes.deposit,
                                "comment":refund_comment,
                                "reference":transcation_id
                                }
    try:
        cur = exec.execute_statement("UPDATE Wallet  set is_deleted = 1 WHERE id = ?",transcation_id)
        refund = exec.execute_statement("INSERT INTO Transcation ?",refund_data)
        update_wallet_balance(exec,wallet_id=refund_data.wallet_id,
                                amount = refund_data.amount,
                                    type= refund_data.type)
        data =refund[FIRST_OBJECT]
        return data
    except:
        return False

def get_transcation(exec,trans_id):
    cur = exec.execute_statement("SELECT * FROM Transcation where id = ?",trans_id)
    data = cur[FIRST_OBJECT]
    return data
