from rest_framework import serializers


class AbsoluteURLImageField(serializers.ImageField):
    def to_representation(self, value):
        if value:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(value.url)
            else:
                return value.url
        return None
