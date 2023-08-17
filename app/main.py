"""This file contains the api function for gherkin generation"""

from enum import Enum
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, validator

from .utils.generate_gherkin import gherkin_from_ml


class GherkinGenerationRequestBody(BaseModel):
    """This is the schema for the gherkin generation request body"""
    domain: str
    requestId: int
    requirementText: str

    @validator("requestId")
    def check_request_id(cls, value):
        """ validating the requestID"""
        if value <= 0:
            raise ValueError("requestId must be a positive integer")
        return value


class GherkinGenerationSuccessResponse(BaseModel):
    """schema for the success response of the gherkin generation """
    status: str
    statusCode: int
    requestId: int
    generatedGherkin: str


class ErrorResponseModel(BaseModel):
    """ This is the error schema for the error responses"""
    status: str
    statusCode: int
    message: str


class ModelMetadataResponse(BaseModel):
    """This is the schema for the response of the metadata"""
    modelName: str
    version: str
    description: str
    author: str
    lastUpdated: str


class StatusCode(Enum):
    """Enum for the various status codes"""
    SUCCESS = 200
    UNPROCESSABLE_ENTITY = 422
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


app = FastAPI()


@app.post("/v1/generate-gherkin", response_model=GherkinGenerationSuccessResponse)
def generate_gherkin_code(
    gherkin_generation_request_body: GherkinGenerationRequestBody,
):
    """
    Generate Gherkin code based on the provided requirement text.
    """
    gherkin_generation_success_response = gherkin_from_ml(
        gherkin_generation_request_body
    )
    return gherkin_generation_success_response


@app.get("/v1/health")
def check_health():
    """ method to check the health of the server"""
    health = {"isAlive": True}
    return health


@app.get("/{version}/model")
async def get_model_metadata(version:str):
    """Method will return the metadata about the ML model"""

    return ModelMetadataResponse(
        modelName="Curiosity Model",
        version="1.0.0",
        description="This is the Curiosity Model\
        used for Gherkin code generation.",
        author="Curiosity",
        lastUpdated="2023-07-26T12:34:56Z",
    )


@app.exception_handler(RequestValidationError)
def unprocessable_entity_exception_handler(response, exception):
    """ Exception handler for error code 422 - unprocessable entity"""
    error_response = ErrorResponseModel(
        status="FAIL",
        statusCode=StatusCode.UNPROCESSABLE_ENTITY.value,
        message=exception.errors()[0]['msg'])
    return JSONResponse(
        content=dict(error_response),
        status_code=StatusCode.UNPROCESSABLE_ENTITY.value)


@app.exception_handler(404)
def not_found_exception_handler(response, exception):
    """ Exception handler for error code 404 - Endpoint not found"""
    error_response = ErrorResponseModel(
        status="FAIL",
        statusCode=StatusCode.NOT_FOUND.value,
        message="Requested Endpoint Not Found")
    return JSONResponse(
        content=dict(error_response),
        status_code=StatusCode.NOT_FOUND.value)


@app.exception_handler(500)
def internal_server_error_exception_handler(response, exception):
    """ Exception handler for error code 500 - internal server error"""
    error_response = ErrorResponseModel(
        status="FAIL",
        statusCode=StatusCode.INTERNAL_SERVER_ERROR.value,
        message="Internal Server Error")
    return JSONResponse(
        content=dict(error_response),
        status_code=StatusCode.INTERNAL_SERVER_ERROR.value)