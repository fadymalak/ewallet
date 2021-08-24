from pydantic import BaseModel ,PositiveFloat 

from enum import Enum
from typing import Any ,Optional 
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

class WalletUpdate(BaseModel):
    id: Any
    balance : Optional[PositiveFloat] 

class Wallet(WalletUpdate):
    mail: str

class ProcessTypes(str,Enum):
    deposit  = "deposit"
    withdraw = "withdraw"

class Transcation(BaseModel):
    wallet_id:int   
    type : ProcessTypes
    amount: PositiveFloat
    date : datetime.datetime = datetime.datetime.now()
    comment: Any
    is_deleted: Optional[int] = 0
    reference : Optional[int] = 0


