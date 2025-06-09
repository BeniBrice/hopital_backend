from rest_framework.response import Response


class ResponseMessage:

    @staticmethod
    def successMessage(
        message,
        data,
        status_code,
    ):
        return Response(
            {
                "message": message,
                "success": True,
                "data": data,
                "status_code": status_code,
            },
            status=status_code,
        )

    @staticmethod
    def error_message(message, data, status_code):
        return Response(
            {
                "message": message,
                "data": data,
                "success": False,
                "status_code": status_code,
            },
            status=status_code,
        )
