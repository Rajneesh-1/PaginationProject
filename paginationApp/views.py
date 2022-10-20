# Create your views here.
import time
from functools import wraps

from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache

from .models import Content
# from .myPagination import MyPageNumberPagination
from .myPagination import MyLimitOffsetPagination
# from .myPagination import MyCursorPagination
from .serializers import ContentSerializer
from rest_framework.filters import SearchFilter


class ContentListCreate(ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    # authentication_classes = [BasicAuthentication]
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = MyLimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ["contentType", "contentSpecificName"]


class ContentRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    #authentication_classes = [BasicAuthentication]
    #permission_classes = [IsAdminUser]


@api_view(['GET'])
def getConfigApi(request):
    if request.method == "GET":
        return Response({'responseCode': 0, 'responseMessage': "Success", 'responseData': []})


@api_view(['GET', 'POST'])
def ContentApiFuncBasedApiView(request, pk=None):
    if request.method == "GET":
        if pk is not None:
            stu = Content.objects.get(id=pk)
            serializer = ContentSerializer(stu)
            return Response(serializer.data)

        stu = Content.objects.all()
        serializer = ContentSerializer(stu, many=True)

        return Response(serializer.data)

    if request.method == "POST":
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class ContentApiClassBasedApiView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            stu = Content.objects.get(id=pk)
            serializer = ContentSerializer(stu)
            return Response(serializer.data)
        stu = Content.objects.all()
        serializer = ContentSerializer(stu, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None, format=None):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data created'}, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
