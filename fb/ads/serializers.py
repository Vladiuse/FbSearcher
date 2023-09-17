from .models import FbGroup
from rest_framework import serializers
from django.core.validators import RegexValidator
from django.utils import timezone


class FbGroupCreateSerializer(serializers.Serializer):
    group_url = serializers.URLField(
        validators=[RegexValidator(regex=FbGroup.FB_GROUP_PATTERN, message='Not valid fb group url')]
    )

    def create(self, validated_data):
        url = validated_data['group_url']
        group_id =  FbGroup.fb_group_url_to_id(url)
        group, created = FbGroup.objects.update_or_create(
            group_id=group_id,
            defaults={'last_ad_date': timezone.now().date()},
        )
        return group