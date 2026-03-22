from app.schemas.common_schema import APIResponse


def success_response(data=None, message="Success"):
    return APIResponse(success=True, message=message, data=data)


def error_response(message="Something went wrong", data=None):
    return APIResponse(success=False, message=message, data=data)
