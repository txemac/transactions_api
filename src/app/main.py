from typing import Dict

from fastapi import FastAPI

from app.api_v1_transactions import api_v1_transactions
from app.api_v1_users import api_v1_users
from database import Base
from database import engine

Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(
        title='Transaction API'
    )

    app.include_router(api_v1_users, prefix='/api/v1/users', tags=['users'])
    app.include_router(api_v1_transactions, prefix='/api/v1/transactions', tags=['transactions'])

    return app


app = create_app()


@app.get('/_check', status_code=200)
def get_check() -> Dict:
    return dict(status='OK')
