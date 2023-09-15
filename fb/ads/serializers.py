from rest_framework import serializers
from .models import FbGroup, FbLibAd
from urllib.parse import urlparse


def clean_fb_group_url(url):
    url = urlparse(url).path
    if url.startswith('/'):
        url = url[1:]
    if url.endswith('/'):
        url =url[:-1]
    return url

class FbLibAdSerializer(serializers.ModelSerializer):

    class Meta:
        model = FbLibAd
        fields = '__all__'
        extra_kwargs = {
            'created': {'read_only': True,},
        }


    def create(self, validated_data):
        ad_data = validated_data['ad']
        fb_group = FbGroupSerializer(data=validated_data)
        fb_group.is_valid(raise_exception=True)
        fb_group.save()
        ad = FbLibAd.objects.get_or_update(**ad_data)
        return ad



class FbGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = FbGroup
        fields = '__all__'

    def create(self, validated_data):
        obj, created = FbGroup.objects.get_or_create(**validated_data)
        return obj


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



