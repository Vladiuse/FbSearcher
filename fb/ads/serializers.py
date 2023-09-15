from rest_framework import serializers
from .models import FbGroup
from urllib.parse import urlparse


def clean_fb_group_url(url):
    url = urlparse(url).path
    if url.startswith('/'):
        url = url[1:]
    if url.endswith('/'):
        url =url[:-1]
    return url


class FbGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FbGroup
        fields = '__all__'

    def to_internal_value(self, data):
        url = data['raw_url']
        data['id'] = clean_fb_group_url(url)
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
