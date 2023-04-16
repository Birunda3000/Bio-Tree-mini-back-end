def response(status: str, message: str, code: int, data: dict = None) -> tuple[dict, int]:
    response_object = {
        "status": status,
        "message": message,
    }
    if data:
        response_object["data"] = data
    return response_object, code