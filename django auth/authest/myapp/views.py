from django.shortcuts import render

# Create your views here.
from django.utils.log import logging
from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)

class DebugView(APIView):

    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get("Authorization", "No Token")
        logger.debug(f"Received Token: {auth_header}")
        return Response({"token": auth_header})