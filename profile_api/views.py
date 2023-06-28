from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import  filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profile_api import serializers 
from profile_api import models
from profile_api import permissions



class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIView features"""
        an_apiview= [
            'uses HTTP methods as function (get , post , patch , put, delete)',
            'is similar to a traditional django view',
            'gives you the most control over you application logic',
            'is mapped manually to URLs',
        ]

        return Response({'message':'Hello!','an_apiview':an_apiview})

    def post(self , request):
        """create a hello message with our name"""
        serializer= self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message= f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
                )

    def put(self , request , pk= None):
        """handle updating an object"""
        return Response({'method':'PUT'})

    def patch(self, request, pk= None):
        """handle a partial update of an object"""
        return Response({'method':'PATH'})
    
    def delete(self,request, pk=None):
        """delete an object"""
        return Response({'method':'Delete'})


class HelloViewSet(viewsets.ViewSet):
    """test api viewset"""
    serializer_class = serializers.HelloSerializer


    def list(self,request):
        """return a hello message"""

        a_viewset=[
        'uses actions (list, create ,retrieve, update, partial_update)',
        'automatically maps to URLs using routers',
        'provides more functionality with less code',
        ]

        return Response({'message':'hello!', 'a_viewset':a_viewset})


    def create(self, request):
        """create a new hello message"""
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'hello {name}!'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status= status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request , pk = None):
        """handle getting an object"""
        return Response({'http_method':'GET'})

    def update(self, request , pk = None):
        """handle updating an object"""
        return Response({'http_message':'PUT'})

    def partial_update(self, request , pk=None):
        """handle updatin part of an object"""
        return Response({'http_message':'PATCH'})

    def destroy (self, request , pk= None):
        """handle removing an object"""
        return Response({'http_message':'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset= models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends=(filters.SearchFilter,)
    search_fields= ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """handle creating user authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet ( viewsets.ModelViewSet):
    """handles creating , reading and updating profile feed items"""
    authentication_classes= (TokenAuthentication,)
    serializer_class= serializers.ProfileFeedItemSerializer
    queryset= models.ProfileFeedItem.objects.all()
    permission_classes= (        permissions.UpdateOwnStatus,IsAuthenticated    )

    def perform_create(self, serializer):
        """sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)