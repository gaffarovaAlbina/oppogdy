from django.shortcuts import renderfrom . import serializersfrom django.contrib.auth.models import Userfrom django.contrib.auth import authenticatefrom django.contrib.auth import login as auth_loginfrom django.contrib.auth import logout as auth_logoutfrom django.views.decorators.csrf import csrf_exemptfrom rest_framework.authtoken.models import Tokenfrom rest_framework.decorators import api_view, permission_classesfrom rest_framework.permissions import AllowAny,IsAuthenticatedfrom rest_framework.status import (    HTTP_400_BAD_REQUEST,    HTTP_404_NOT_FOUND,    HTTP_200_OK)from rest_framework.response import Responsefrom rest_framework import generics, permissionsclass UserList(generics.ListAPIView):	queryset = User.objects.all()	serializer_class = serializers.UserSerializer	permission_classes = [permissions.IsAdminUser]class UserDetail(generics.RetrieveAPIView):	queryset = User.objects.all()	serializer_class = serializers.UserSerializer	permission_classes = [permissions.IsAdminUser]	def retrieve(self, request, *args, **kwargs):		instance = User.objects.get(id=request.headers['userId'])		serializer = self.get_serializer(instance)		return Response(serializer.data)@csrf_exempt@api_view(["POST"])@permission_classes((AllowAny,))def login(request):    username = request.data.get("username")    password = request.data.get("password")    if username is None or password is None:        return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)    user = authenticate(username=username, password=password)    if not user:    	return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)    auth_login(request, user)    token, _ = Token.objects.get_or_create(user=user)    return Response({'detail': 'Token was sent.'}, headers={'token': token.key}, status=HTTP_200_OK)@csrf_exempt@api_view(["GET"])@permission_classes((IsAuthenticated,))def logout(request):    if not request.user:        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)    try:    	request.user.auth_token.delete()    except:    	return Response({'error': 'Invalid Credentials'}, status=HTTP_400_BAD_REQUEST)    auth_logout(request)    return Response({'detail': 'Successfully logged out.'}, status=HTTP_200_OK)