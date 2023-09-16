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

class FbAddChoiceCustomField(serializers.ChoiceField):

    def to_internal_value(self, data):
        if data == FbLibAd.ACTIVE:
            data = '1'
        if data == FbLibAd.NOT_ACTIVE:
            return '0'
        return data


class FbLibAdCreateSerializer(serializers.Serializer):
    status = FbAddChoiceCustomField(choices=FbLibAd.AD_STATUS)
    group_url = serializers.URLField()
    time_text = serializers.CharField()
    id = serializers.IntegerField()

    def create(self, validated_data):
        print(validated_data)
        fb_group_url = validated_data.pop('group_url')
        group_data = {'raw_url': fb_group_url}
        fb_group = FbGroupSerializer(data=group_data)
        fb_group.is_valid(raise_exception=True)
        fb_group.save()
        ad = FbLibAd.objects.get_or_update(group=fb_group,**validated_data)
        return ad

class FbGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = FbGroup
        fields = '__all__'

    # def create(self, validated_data):
    #     obj, created = FbGroup.objects.update_or_create(**validated_data)
    #     return obj


    def to_internal_value(self, data):
        print('to_internal_value')
        url = data['raw_url']
        data['id'] = clean_fb_group_url(url)
        return super().to_internal_value(data)

    def validate_raw_url(self, value):
        print('validate_raw_url', value)
        if urlparse(value).netloc != FbGroup.GROUP_DOMAIN:
            raise serializers.ValidationError(f'incorrect group domain url: "{value}"')
        return value

    def validate_name(self, value):
        return value.strip()

    def validate_address(self, value):
        return value.strip()

    def validate_email(self, value):
        return value.strip()



