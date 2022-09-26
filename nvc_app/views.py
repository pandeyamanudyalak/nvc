import email
from django.contrib.auth.models import Group
from multiprocessing import context
from tokenize import group
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from nvc_app import serializers
from nvc_app.serializers import SendPasswordResetEmailSerializer, TicketSerializer, UserLoginSerializer, UserRegistrationSerializer , UserPasswordResetSerializer , UserChangePasswordSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import TicketModel, User
from django.contrib.auth.hashers import make_password


# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    # email = serializer.data.get('email')
    # group = Group.objects.get_or_create(name='Engnieer')
    # user = User.objects.get(email=email)
    
   
    
    #token = get_tokens_for_user(user)
    return Response({ 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    print(email)
    password = serializer.data.get('password')
    print(password)
    user = authenticate(email=email, password=password)
    
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class EmailPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self,request,*args,**kwargs):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    if serializer.is_valid():
      print(serializer.data)
      email = serializer.data.get('email')
      return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
  renderer_classes = [UserRenderer]
  def post(self,request,*args,uid,token,**kwargs):
    serializer = UserPasswordResetSerializer(data = request.data,context={"uid":uid,"token":token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Done'}, status=status.HTTP_200_OK)



class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated,]
  def post(self,request,*args,format=None,**kwargs):
    serializer = UserChangePasswordSerializer(data=request.data,context={"user":request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Your password changed successfully.'}, status=status.HTTP_200_OK)


class CreateTicket(APIView):
  renderer_classes = [UserRenderer]
  def post(self,request,*args,**kwargs):
    file = request.FILES.getlist('attach_file')
   
    serializer = TicketSerializer(data=request.data,context={'file':file})
    
    
    if serializer.is_valid():
      
      serializer.save()
      
      return Response({'msg':'Ticket created successfully.'}, status=status.HTTP_201_CREATED)
    return Response({'msg':'Something wents wrong.'}, status=status.HTTP_400_BAD_REQUEST)


class AllTickets(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated,]
  def get(self,request):
    p = request.user.get_group_permissions()
    print('-----------0ppppppp----------0',p)
    #print('++++++++++++++',serializer.data.get['attach_file'])
   
    ticket_data = TicketModel.objects.all()
    serializer = TicketSerializer(ticket_data,many=True)
    return Response(serializer.data)


class OnCallView(APIView):
  def get(self,request):
    on_call_tickets = TicketModel.objects.filter(on_call_ticket=True)
    serializer = TicketSerializer(on_call_tickets,many=True)
    return Response(serializer.data)

class ClosedTicketView(APIView):
  def get(self,request):
    closed_tickets = TicketModel.objects.filter(closed_ticket=True)
    serializer = TicketSerializer(closed_tickets,many=True)
    return Response(serializer.data)

class VisitAndClosedView(APIView):
  def get(self,request):
    visit_and_closed_tickets = TicketModel.objects.filter(visit_and_closed=True)
    serializer = TicketSerializer(visit_and_closed_tickets,many=True)
    return Response(serializer.data)
  
from .serializers import FileListSerializer

from rest_framework.parsers import MultiPartParser, FormParser

from .models import Photo
from rest_framework import viewsets
  
class PhotoViewSet(viewsets.ModelViewSet):
  serializer_class = TicketSerializer
  parser_classes = (MultiPartParser, FormParser,)
  queryset=TicketModel.objects.all()