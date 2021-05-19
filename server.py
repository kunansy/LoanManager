#!/usr/bin/env python3
import os
import sys

from sanic import Sanic, Request, HTTPResponse, response
from sanic_openapi import swagger_blueprint, doc
from pydantic import BaseModel, constr, ValidationError

from src import db_api


app = Sanic(__name__)
app.blueprint(swagger_blueprint)


class Loan(BaseModel):
    product_name: constr(strip_whitespace=True, min_length=1)


class LoanSchema:
    id = doc.Integer(description="UUID of the loan")
    productionName = doc.String(description="Name of the production")


@app.post('/loans')
@doc.summary("Add a loan")
@doc.consumes(doc.String(name="product_name"), location="body", required=True)
@doc.response(200, {}, description="The loan added")
@doc.response(400, {}, description="Validation error, wrong production name")
async def add_loan(request: Request) -> HTTPResponse:
    try:
        loan = Loan(product_name=request.body)
    except ValidationError as e:
        print(repr(e), file=sys.stderr)
        return response.json(e.json(), status=400)

    db_api.add_loan(product_name=loan.product_name)
    return HTTPResponse(status=200)


@app.get('/loans/<loan_id:int>')
@doc.summary("Get the loan")
@doc.consumes(doc.Integer(name="loan_id"), location="query")
@doc.produces(LoanSchema)
@doc.response(404, {}, description="Loan with id not found")
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
