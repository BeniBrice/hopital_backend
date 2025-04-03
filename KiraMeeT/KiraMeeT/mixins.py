from rest_framework import status
from rest_framework.response import Response
from e_commerce.response_message import ResponseMessage
from django.shortcuts import get_object_or_404


class CustomPaginationMixin:

    def get_paginated_response(self, data):
        paginated_data = super().get_paginated_response(data)
        paginated_data.data["object_count"] = (
            self.get_queryset().filter(is_read=False).count()
        )
        return ResponseMessage.successMessage(
            message="Data fetched successfully",
            data=paginated_data.data,
            status_code=status.HTTP_200_OK,
        )


class ListCustomPaginationMixin:

    def get_paginated_response(self, data):
        paginated_data = super().get_paginated_response(data)
        paginated_data.data["object_count"] = self.get_queryset().count()
        return ResponseMessage.successMessage(
            message="Data fetched successfully",
            data=paginated_data.data,
            status_code=status.HTTP_200_OK,
        )


class DeleteMixin:
    """mixins for delete operation"""

    def delete_object(
        self,
        request,
        username,
        model,
        object_id,
        user,
        user_field=None,
    ):

        try:

            if user_field:
                print(f"delete an object wich belong to {username}")
                kwargs = {
                    "id": object_id,
                    user_field: user,
                }

                object = get_object_or_404(model, **kwargs)

            else:
                print(f"delete an specific object with id {object_id}")
                object = get_object_or_404(model, id=object_id)

            # delete object
            object.delete()
            return ResponseMessage.successMessage(
                message="Object deleted successfully",
                data={},
                status_code=status.HTTP_204_NO_CONTENT,
            )

        except Exception as e:
            return ResponseMessage.error_message(
                message=str(e),
                data={},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
