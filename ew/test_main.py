from fastapi.testclient import TestClient
from fastapi import status
from .main import app
from .database2 import Base
from .main import get_db
client = TestClient(app)    
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import pytest
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

#overwrite to test database
app.dependency_overrides[get_db] = override_get_db
global wallet_id
wallet_id = 0
def test_create_new_wallet():
    global wallet_id
    res = client.post("/wallet",json={"mail":"fadytest2","balance":20})
    assert res.status_code == 200
    wallet_id = res.json()['id']
    res= client.get("/wallet/"+str(wallet_id))
    assert res.status_code==200
    assert res.json()["mail"]=="fadytest2"
    res = client.put("/wallet/",json={"wallet_id":wallet_id,"amount":20,"type":"deposit"})
    assert status.HTTP_200_OK==res.status_code
    
def test_get_invaild_wallet():
    res = client.get("/wallet/2")
    assert res.status_code==status.HTTP_404_NOT_FOUND
def test_update_invalid_type():
    res = client.put("/wallet/",json={"wallet_id":"111","amount":20,"type":"deosit"})
    assert status.HTTP_422_UNPROCESSABLE_ENTITY==res.status_code

def test_create_transcation():
    res = client.post("/transcation",json={"wallet_id":wallet_id,"amount":20,"type":"deposit"})

    assert res.status_code == 200
def test_refund_transcation():
    res1 = client.get("/transcation/1")
    res = client.delete("/transcation/1")
    assert res.status_code==200
    assert res.json()['type'] == "deposit"
    assert res.json()['amount'] == res1.json()['amount']


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    def remove_test_dir():
        os.remove("test.db")
    request.addfinalizer(remove_test_dir)
