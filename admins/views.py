from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Admin
from .serializers import AdminSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'first_name', 'last_name', 'post']

    def get_permissions(self):
        """
        Définir des permissions différentes pour chaque méthode.
        """
        if self.action in ['create', 'list']:
            return [AllowAny()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return []

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Authentification par email, mot de passe et post.
        """
        email = request.data.get('email')
        password = request.data.get('password')
        post = request.data.get('post')

        admin = Admin.objects.filter(email=email, post=post).first()

        if admin and admin.check_password(password):
            # Générer les tokens
            refresh = RefreshToken.for_user(admin)
            access_token = RefreshToken.access_token
            return Response({
                'refresh': str(refresh),
                'access': str(access_token),
                'message': f'Bienvenue {admin.first_name}!'
            }, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Permet la recherche d'admins.
        """
        query = request.query_params.get('q', '')
        admins = self.queryset.filter(
            first_name__icontains=query
        ) | self.queryset.filter(
            last_name__icontains=query
        ) | self.queryset.filter(
            email__icontains=query
        ) | self.queryset.filter(
            post__icontains=query
        )
        serializer = self.get_serializer(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
