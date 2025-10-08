from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import views
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import CustomUserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.follow(target_user)
        return Response({"detail": f"You are now following {target_user.username}."})


class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        request.user.unfollow(target_user)
        return Response({"detail": f"You have unfollowed {target_user.username}."})
                         
# User = get_user_model()


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = [permissions.AllowAny]
#     serializer_class = RegisterSerializer


# def create(self, request, *args, **kwargs):
#     serializer = self.get_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.save()
#     token, _ = Token.objects.get_or_create(user=user)
#     data = UserSerializer(user, context={'request': request}).data
#     data['token'] = token.key
#     return Response(data, status=status.HTTP_201_CREATED)




# class CustomObtainAuthToken(ObtainAuthToken):
#     permission_classes = [permissions.AllowAny]


#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         token = Token.objects.get(key=response.data['token'])
#         user = token.user
#         data = {
#             'token': token.key,
#             'user': UserSerializer(user, context={'request': request}).data
#             }
#         return Response(data)


# class ProfileView(APIView):
#     permission_classes = [IsAuthenticated]


#     def get(self, request):
#         serializer = UserSerializer(request.user, context={'request': request})
#         return Response(serializer.data)


#     def put(self, request):
#         serializer = UserSerializer(request.user, data=request.data, partial=True, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
