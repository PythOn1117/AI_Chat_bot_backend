from django.http import JsonResponse


def set_response(data):
    return JsonResponse(
        {
            "code": 0,
            "message": data.get("message", ""),
            "data": data.get("data", {})
        }
    )


def set_error(error_msg):
    return JsonResponse(
        {
            "code": 1,
            "message": error_msg,
            "data": {}
        }
    )