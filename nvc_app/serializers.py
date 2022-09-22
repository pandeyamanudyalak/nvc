from urllib import request
from xml.dom import ValidationErr
from rest_framework import serializers
from nvc_app.models import TicketModel, User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'user_name', 'password', 'password2', 'user_city','user_zip_code','user_company_name']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
   
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    print('--------EMail',email)
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      print('----------------User inside if',user)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:8000/reset_password/'+uid+'/'+token
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  new_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['new_password', 'confirm_password']

  def validate(self, attrs):
    try:
      password = attrs.get('new_password')
      password2 = attrs.get('confirm_password')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("new_password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')


class TicketSerializer(serializers.ModelSerializer):
  class Meta:
    model = TicketModel
    fields = ('query_type','ticket_creator_name','ticket_email','ticket_creator_address','equipment_name','equipment_sr_no','equipment_model_no','problem_description','production_temprorary_running','running_with_rejection','production_breakdown','sales_production_name','process_mc_type','max_kg_or_hrs','material_denticty','virgin','regrind','falkes','master_batch','additives_1','additives_2','work_order_no','packing_slip_no','receive_in_good_condition','equipment_description','production_trial_readliness_date','pending','ready','during_engg_visit','not_understood_list','further_tech_guidence_needed','spare_name','spare_sr_no','spare_model_name','part_name','part_description','part_quantity','closed_ticket','on_call_ticket','visit_and_closed','visit_scheduled','waiting_for_spares')

 

 

  
