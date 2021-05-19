#!/usr/bin/env python3
import os

from sanic import Sanic, Request, HTTPResponse, response
from sanic_openapi import swagger_blueprint
from pydantic import BaseModel, constr

from src import db_api


app = Sanic(__name__)
app.blueprint(swagger_blueprint)


class Loan(BaseModel):
    product_name: constr(strip_whitespace=True, min_length=1)


@app.post('/loans')
async def add_loan(request: Request) -> HTTPResponse:
    pass


@app.get('/loans/<loan_id:int>')
async def get_loan(request: Request,
                   loan_id: int) -> HTTPResponse:
    if (loan := db_api.get_loan(loan_id=loan_id)) is None:
        return HTTPResponse(status=404)

    return response.json(loan.json())


if __name__ == "__main__":
    app.run(
        port=8081,
        workers=os.cpu_count(),
        access_log=False
    )
