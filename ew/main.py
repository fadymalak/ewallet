from logging import debug
from fastapi import FastAPI ,HTTPException,status , Body,Depends
from .schemas import ProcessTypes, Transcation,Wallet,generate_unique_id,WalletUpdate
from pydantic import PositiveFloat
from .database2 import SessionLocal
from sqlalchemy.orm import Session
from . import crud2
import uvicorn
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/wallet/{wallet_id}")
def wallet_info(wallet_id:int,db:Session=Depends(get_db)):
    """
    Get Wallet Information

    \f
    :param ww : Wallet ID
    """
    response = crud2.get_wallet(db,wallet_id)
    if response:
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
@app.post("/wallet")
def create_wallet(wallet:Wallet,db:Session=Depends(get_db)):
    wallet.id = generate_unique_id()
    data = crud2.create_wallet(db,wallet)
    if data:
        return data
    raise HTTPException(status_code=status.HTTP_302_FOUND)

@app.put("/wallet/")    
def update_wallet(wallet_id:int=Body(...),
                    amount:PositiveFloat=Body(...),
                        type:ProcessTypes=Body(...),
                        db:Session=Depends(get_db)):
    """
    Recharge Wallet Only
    """
    data = crud2.update_wallet_balance(db,wallet_id=wallet_id,amount=amount,type=type)
    if data:
        return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete("/wallet/{wallet_id}")
def delete_wallet(wallet_id:int):
    pass

@app.post("/transcation")
def create_transcation(trans:Transcation,db:Session=Depends(get_db)):
    trans = crud2.make_transcation(db,trans)
    if trans:
        return trans
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)

@app.get("/transcation/{trans_id}")
def get_transcation_info(trans_id:int,db:Session=Depends(get_db)):
    data =crud2.get_transcation(db,trans_id)
    if data:
        return data
    raise  HTTPException(status_code =status.HTTP_404_NOT_FOUND)

@app.delete("/transcation/{trans_id}")
def update_transcation(trans_id:int,db:Session=Depends(get_db)):
    data = crud2.delete_transcation(db,transcation_id=trans_id)
    return data

