from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import FbLibAdSerializer, FbGroupSerializer
from rest_framework.response import Response
from rest_framework import status
import json


class FbGroupMAssCreateView(APIView):


    def post(self, request, format=None):
        invalid_data = []
        data = request.data['items']
        for ad in data:
            raw_url = ad.pop('raw_url')
            name = ad.pop('name')
            group_data = {
                'raw_url': raw_url,
                'name': name,
                'ad': [ad,]
            }
            serializer = FbGroupSerializer(data=group_data)
            if serializer.is_valid():
                serializer.save()
            else:
                invalid_data.append(group_data)
        return Response({'x': invalid_data},status=status.HTTP_200_OK)
