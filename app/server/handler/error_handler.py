import contextlib
import time
from typing import Any

from app.server.logger.custom_logger import logger, logging_api_requests
from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import JWTError


class UnAuthorisedError(Exception):
    """UnAuthorised exception"""


class ForbiddenError(Exception):
    """Forbidden exception"""


class CustomException(Exception):
    """Our own custom exception for throwing errors with specific message and errorCode"""

    def __init__(self, error_data: dict[str, Any]):
        self.error_code = error_data['errorCode']
        self.message = error_data['message']


async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    """Exception handler to handle Request validation errors
    Args:
        request (Request): Request object
        exc (RequestValidationError): Exception object

    Returns:
        JSONResponse: Returns error data in the desired format
    """

    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=get_error_response('Request validation error', status.HTTP_422_UNPROCESSABLE_ENTITY, exc.errors()))


async def custom_exception_handler(_request: Request, exc: CustomException) -> JSONResponse:
    """Exception handler to handle exception of type CustomException
    Args:
        request (Request): Request object
        exc (CustomException): Exception object

    Returns:
        JSONResponse: Returns error data in the desired format
    """
    return JSONResponse(status_code=status.HTTP_200_OK, content=get_error_response(exc.message, exc.error_code))


async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    """Exception handler to handle exception of type HTTPException
    Args:
        request (Request): Request object
        exc (HTTPException): Exception object

    Returns:
        JSONResponse: Returns error data in the desired format
    """
    code = exc.status_code or status.HTTP_404_NOT_FOUND
    headers = {}
    with contextlib.suppress(AttributeError):
        headers = exc.headers
    return JSONResponse(status_code=code, content=get_error_response(exc.detail, code), headers=headers)


async def catch_exceptions_middleware(request: Request, call_next) -> JSONResponse:
    """Middleware to catch all the Exceptions and send API process time over response headers"""
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        logging_api_requests(request, response)
        return response
    except JWTError as error:
        logger.debug(str(error))
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=get_error_response(str(error), status.HTTP_401_UNAUTHORIZED))
    except UnAuthorisedError as error:
        logger.debug(str(error))
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=get_error_response(str(error), status.HTTP_401_UNAUTHORIZED))
    except ForbiddenError as error:
        logger.debug(str(error))
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=get_error_response(str(error), status.HTTP_403_FORBIDDEN))
    except Exception as error:
        logger.debug(str(error))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=get_error_response(str(error), status.HTTP_500_INTERNAL_SERVER_ERROR))


def get_error_response(message: str, code: int, detail: Any = None) -> dict[str, Any]:
    """Function to format error data

    Args:
        message (str): Error message
        code (int): Error code

    Returns:
        JSON: Returns error data in the desired format
    """
    error = {'status': 'FAIL', 'errorData': {'errorCode': code, 'message': message}}
    if detail:
        error['errorData'].update({'detail': detail})
    return jsonable_encoder(error)
