from rest_framework import serializers
from .models import FbGroup
from urllib.parse import urlparse


class FbGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FbGroup
        fields = '__all__'

    def to_internal_value(self, data):
        data['id'] = urlparse(data['raw_url']).path
        if data['id'].startswith('/'):
            data['id'] = data['id'][1:]
        if data['id'].endswith('/'):
            data['id'] = data['id'][:-1]
        return super().to_internal_value(data)

    def validate_raw_url(self, value):
        if urlparse(value).netloc != FbGroup.GROUP_DOMAIN:
            raise serializers.ValidationError(f'incorrect group domain url: "{value}"')
        return value

    def validate_name(self, value):
        return value.strip()

    def validate_address(self, value):
        return value.strip()

    def validate_email(self, value):
        return value.strip()
