from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, permissions, authentication

from firebase_admin import auth

from .serializers import (UserSerializer, LoginSocialSerializer)
from app.user.models import User



class UserCreateView(generics.CreateAPIView):
    """ Creation d'user """

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if request.data['password'] != request.data['passwordConfirm']:
            raise execption('Not the same password')

        response = super().post(request, *args, **kwargs)
        token = Token.objects.get_or_create(user_id=response.data['id'])
        return Response({
            'token': str(token[0]),
            'user': response.data,
            'status': status.HTTP_201_CREATED
        })


class GoogleLoginView(APIView):
    """ Login avec Google et le sauvegarder dans notre bdd """

    serializer_class = LoginSocialSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, **validated_data):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_token = serializer.data.get('token_id')
        
        decoded_token = auth.verify_id_token(id_token)

        email = decoded_token['email']
        name = decoded_token['name']
        avatar = decoded_token['picture']
        split_name = name.split()

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
        else:
            user, created = User.objects.get_or_create(
                email=email,
                username=name,
                first_name=split_name[0],
                last_name=split_name[1],
                is_active=True,)

            if created:
                token = Token.objects.create(user=user)
        
        token = Token.objects.get_or_create(user=user)
        serializer_user = UserSerializer(user, context={'request': request})

        return Response({'token': str(token[0]), 'user': serializer_user.data, 'status': status.HTTP_200_OK})
 

class GetAuthTokenAndData(ObtainAuthToken):
    """ Céer un token et l'ajoute à l'utilisateur """

    def post(self, request, *args, **kwargs):
        user = authenticate(
            email=request.data['email'], password=request.data['password'])
        
        user_serializer = UserSerializer(
            user, many=False, context={'request': request})
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            return Response({
                'token': str(token[0]),
                'user': user_serializer.data})
        return super(GetAuthTokenAndData, self).post(request, *args, **kwargs)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Premet de manage l'utilisateur connecté  API sécurisée (besoin de Token )
    """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)



    def get(self, request, *args, **kwargs):
        response = super(ManageUserView, self).get(request, *args, **kwargs)
        user = User.objects.get(id=response.data['id'])
        token = Token.objects.get(user_id=response.data['id'])
        user_serializer = UserSerializer(
            user, many=False, context={'request': request})
        return Response({
            'token': token.key, 
            'user': user_serializer.data,
            'status': status.HTTP_200_OK
            })

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        user = User.objects.get(pk=response.data['id'])
        token = Token.objects.get(user_id=response.data['id'])
        user_serializer = UserSerializer(
            user, 
            many=False,
            context={'request': request}
        )
        return Response({
            'token': token.key, 
            'user': user_serializer.data,
            'status': status.HTTP_200_OK
        })

    def get_object(self):
        return self.request.user