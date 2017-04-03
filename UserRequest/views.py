from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Import the email modules we'll need

from django.views.decorators.csrf import csrf_exempt
from .models import Request
from .serializer import UserRequestSerializer
from rest_framework import status
from zipcode_distance import distance
from dentist_login.models import Dentist
from UserLogin.models import UserLogin
import unicodedata
import threading


# Create your views here.

class UserRequest(APIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    user_name = ""


    @csrf_exempt
    def post(self, request):
        serializer = UserRequestSerializer(data=request.data)
        if serializer.is_valid():

            data = serializer.validated_data
            title =  data.get("request_title",'')
            desc = data.get('request_desc','')
            user_email = data.get('request_user','')

            dentist_email = self.get_dentist(user_email,serializer)
            serializer.save()
            if dentist_email != "":
                self.send_html_mail(title,desc,user_email, dentist_email,self.user_name)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @csrf_exempt
    def get(self, request):
        id =  self.request.query_params.get('id', '')
        user = UserLogin.objects.all().filter(fbuserId=id)
        if(len(user)>0):
            user_requests = Request.objects.all().filter(request_user=user[0].email).order_by('-check_in')
            return Response(user_requests.values(), status=status.HTTP_201_CREATED)
        return Response([], status=status.HTTP_200_OK)



    def get_dentist(self, email,serializer):
        dentist = Dentist.objects.all()
        user = UserLogin.objects.filter(email=email)[:1]

        if(len(user) == 0):
            return "";
        self.user_name = user[0].first_name;
        user_dentist = user[0].user_dentist
        # if user_dentist != None:
        #     return user[0].user_dentist.email
        if user != None:
            count = dentist.count()
            user_zip = user[0].zip

            i = 0
            while i < count:
                dentist_item = dentist[i]
                i = i+1
                if(dentist_item.active == False):
                   continue
                # dentist_zip = dentist_item.zip
                # dentist_zip = unicodedata.normalize('NFKD', dentist_zip).encode('ascii','ignore')
                # if(dentist_zip == None or dentist_zip == ""):
                #     continue;
                # user_zip = unicodedata.normalize('NFKD', user_zip).encode('ascii','ignore')
                # if(user_zip == None or user_zip == ""):
                #     return dentist_item.email
                # Commenting for now
                # dist = self.checkDistance(dentist_zip,user_zip)
                # if(dist > 50):
                #     pass
                # else:
                dentist_email = dentist_item.email
                user[0].user_dentist = dentist_item
                serializer.validated_data['request_dentist'] = dentist_item
                user[0].save()

                return dentist_email

        return ""
    def send_html_mail(self,subject, html_content,user_email, recipient_list,user_name):
        EmailThread(subject, html_content, user_email, recipient_list,user_name).start()


    # @csrf_exempt
    # def get(self,request,format=None):
    #     requests = Request.objects.all()
    #     serializer = UserRequestSerializer(requests, many=True)
    #     return Response(serializer.data)

    def checkDistance(self, user_zip, dentist_zip):
        return distance(user_zip,dentist_zip)



    # def sendEmail(self,title,desc,user_email, dentist_email):





class EmailThread(threading.Thread):
    def __init__(self, subject, desc, user_email, recipient_list, user_name):
        self.subject = subject
        self.recipient_list = recipient_list
        self.desc = desc
        self.user_email = user_email
        self.user_name = user_name
        threading.Thread.__init__(self)

    def request_receipt(self, user_email):
        admin_email = 'support@dentalcareapp.com'
        title = "DentalCareApp Request Received"
        desc = "Hi " + self.user_name + "\n\n" \
               "Your request has been received and will be reviewed by our expert dentist shortly. Our dentist will contact you in a timely manner. " \
               "Incase of dental emergency, please contact support@dentalcareapp.com or visit your local dentist.\n\n" \
               "Thank You\n" \
               "DentalCareApp"
        # user_email = "jasmeet.androiddev@gmail.com"
        send_mail(title, desc, admin_email,[user_email],
     fail_silently=True)

    def run (self):
        # dentist_email = "jasmeet.manak@gmail.com"
        self.request_receipt(self.user_email)
        subject = "DentalCareApp Request: " + self.user_name + " with issue  " + self.subject
        full_desc = "You have received a request from " + self.user_name + ":" + "\n\n" + self.desc + "\n\n Please reply to the patient at his email  "+ self.user_email + " in a timely manner. \n\n" \
                                                                                                                                                                    "Thank You \n DentalCareApp"
        send_mail(subject, full_desc, self.user_email,[self.recipient_list],
     fail_silently=True)

























