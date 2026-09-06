from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: object | None = None
