from fastapi import FastAPI, status, Request
from fastapi.exceptions import ResponseValidationError, RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import TimeoutError

def register_exception_handler(app: FastAPI):
    @app.exception_handler(ResponseValidationError)
    async def response_exception_handler(request: Request, exc: ResponseValidationError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'detail': 'Server response error'
            }
        )

    @app.exception_handler(TimeoutError)
    async def timeouterror_exception_handler(request: Request, exc: TimeoutError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                'detail': 'Out of server resources'
            }
        )

    @app.exception_handler(RequestValidationError)
    async def requestvalidation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'detail': 'Error in user request',
                'body': exc.errors()
            }
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        errors = []
        for err in exc.errors():
            errors.append({
                "field": err["loc"][-1],
                "message": err["msg"]
            })
        return JSONResponse(
            status_code=422,
            content={"detail": errors}
        )