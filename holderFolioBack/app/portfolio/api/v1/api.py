from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status, generics, permissions, authentication
from rest_framework import generics, authentication, status

from .serializers import (PortFolioSerializer)
from app.portfolio.models import PortFolio
from app.user.models import User

class PortFolioCreateView(generics.CreateAPIView):
    """API qui permet de créer un portfolio"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PortFolioSerializer


    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                request.data['name']
                if request.data['name'] == '':
                    return Response({'status_code': status.HTTP_400_BAD_REQUEST,})
            except: 
                return Response({'status_code': status.HTTP_400_BAD_REQUEST,})
            isExist = PortFolio.objects.filter(Q(name= request.data['name']), Q(user=request.user)).exists()
            if isExist == False:
                folio = PortFolio.objects.create(
                    user= request.user,
                    name= request.data['name']
                )
                serializer = PortFolioSerializer(folio, context={'request': request})
                return Response({
                    'status_code': status.HTTP_201_CREATED,
                    'portfolio': {
                        'pk': serializer.data.get('pk'),
                        'name': serializer.data.get('name'),
                        'user': serializer.data.get('user')
                    }})
            else:
                return Response({'status_code': status.HTTP_400_BAD_REQUEST, 'error': 'Portfolio name exists'})
        return super().post(request, *args, **kwargs)

class PortFolioRetriveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """API qui permet de retrive un portfolio"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PortFolioSerializer
    queryset =  PortFolio.objects.all()

class PortFolioListView(generics.ListAPIView):
    """ Retourn tous les portfolio lié à un user"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PortFolioSerializer

    def get_queryset(self):
        return PortFolio.objects.filter(user=self.request.user)