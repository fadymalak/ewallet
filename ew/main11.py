from logging import debug
from os import remove
from fastapi import FastAPI ,HTTPException,status , Body
from .schemas import ProcessTypes, Transcation,Wallet,generate_unique_id,WalletUpdate
from .database import driver
from . import crud
import uvicorn
app = FastAPI()

@app.get("/wallet/{wallet_id}")
def wallet_info(wallet_id:int):
    return True

@app.post("/wallet")
def create_wallet(wallet:Wallet):  
    wallet.id = generate_unique_id()
    driver.execute_lambda(lambda exec: crud.create_wallet(exec,wallet))
    return wallet

@app.post("/transcation")
def create_transcation(trans:Transcation):
    driver.execute_lambda(lambda exec: crud.make_transcation(exec,trans))
    return trans

@app.get("/transcation/{trans_id}")
def get_transcation_info(trans_id:int):
    data = driver.execute_lambda(lambda exec: crud.get_transcation(exec,trans_id))
    if data:
        return data
    raise  HTTPException(status_code =status.HTTP_404_NOT_FOUND)

@app.delete("/transcation/{trans_id}")
def update_transcation(trans_id:int):
    data =driver.execute_lambda(lambda exec: crud.delete_transcation(exec,transcation_id=trans_id))
    if data:
        return data
    raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE)

