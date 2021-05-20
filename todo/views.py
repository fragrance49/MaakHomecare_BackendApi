# from django.db.models.fields import json
import json
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
# More rest imports as needed
from django.contrib.auth import authenticate
from datetime import date, timedelta
from .decorators import define_usage
from .models import Services, Members, Task, Booking
from .serializers import servicesSerializer, membersSerializer, taskSerializer, bookingSerializer
from django.contrib.auth.models import User


#URL /
@define_usage(returns={'url_usage': 'Dict'})
@api_view(['GET'])
@permission_classes((AllowAny,))
def api_index(requet):
    details = {}
    for item in list(globals().items()):
        if item[0][0:4] == 'api_':
            if hasattr(item[1], 'usage'):
                details[reverse(item[1].__name__)] = item[1].usage
    return Response(details)


#URL /signin/
#Note that in a real Django project, signin and signup would most likely be
#handled by a seperate app. For signup on this example, use the admin panel.
@define_usage(params={'username': 'String', 'password': 'String'},
              returns={'authenticated': 'Bool', 'token': 'Token String'})
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_signin(request):
    try:
        username = request.data['username']
        password = request.data['password']
    except:
        return Response({'error': 'Please provide correct username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'authenticated': True, 'token': "Token " + token.key})
    else:
        return Response({'authenticated': False, 'token': None})


#URL /all/
@define_usage(returns={'tasks': 'Dict'})
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_all_tasks(request):
    tasks = taskSerializer(request.user.task_set.all(), many=True)
    return Response({'tasks': tasks.data})


#URL /new/
@define_usage(params={'description': 'String', 'due_in': 'Int'},
              returns={'done': 'Bool'})
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_new_task(request):
    task = Task(user=request.user,
                description=request.data['description'],
                due=date.today() + timedelta(days=int(request.data['due_in'])))
    task.save()
    return Response({'done': True})


#URL /update/
@define_usage(params={'task_id': 'Int', 'description': 'String', 'due_in': 'Int'},
              returns={'done': 'Bool'})
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_update_task(request):
    task = request.user.task_set.get(id=int(request.data['task_id']))
    try:
        task.description = request.data['description']
    except: #Description update is optional
        pass
    try:
        task.due = date.today() + timedelta(days=int(request.data['due_in']))
    except: #Due date update is optional
        pass
    task.save()
    return Response({'done': True})


#URL /delete/
@define_usage(params={'task_id': 'Int'},
              returns={'done': 'Bool'})
@api_view(['DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_delete_task(request):
    task = request.user.task_set.get(id=int(request.data['task_id']))
    task.delete()
    return Response({'done': True})



#URL /signup/
#Note that in a real Django project, signin and signup would most likely be
#handled by a seperate app. For signup on this example, use the admin panel.
@define_usage(params={'firstname': 'String', 'lastname': 'String', 'username': 'String', 'email': 'String','password': 'String'},
              returns={'authenticated': 'Bool', 'token': 'Token String'})
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_signup(request):
    try:
        firstname = request.data['firstname']
        lastname = request.data['lastname']
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        birthday = request.data['birthday']
        gender = request.data['gender']
        phonenumber = request.data['phonenumber']

    except:
        return Response({'error': 'Please provide correct username and password'},
                        status=HTTP_400_BAD_REQUEST)
    members = Members.objects.filter(username=username)
    if members.count() > 0:
        resp_er = {'result_code': '101'}
        return HttpResponse(json.dumps(resp_er))
   
    member = Members()
    member.firstname = firstname
    member.lastname = lastname
    member.username = username
    member.email = email
    member.password = password
    member.birthday = birthday
    member.gender = gender
    member.phonenumber = phonenumber

    member.save()

    resp = {'result_code': '0', 'member_id':member.pk}
    return HttpResponse(json.dumps(resp), status = HTTP_200_OK)


@permission_classes((AllowAny,))
@api_view(['POST'])
def loginByUsername(request):   
    
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    
    members = Members.objects.filter(username=username, password=password)
    if members.count() > 0:
        member = members[0]
        data = {
            'id':member.pk,
            'firstname':member.firstname,
            'lastname':member.lastname,
            'username':member.username,
            'email':member.email,
            'password':member.password,
            'birthday':member.birthday,
            'gender':member.gender,
            'phonenumber':member.phonenumber
        }
        resp = {'result_code': '0', 'data':data}
    else:
        resp = {'result_code':'1'}
    return HttpResponse(json.dumps(resp))

@api_view(['POST'])
@permission_classes((AllowAny,))
def getServices(request):
    services = Services.objects.all().order_by('-id')
    serializer = servicesSerializer(services, many=True)
    resp = {'result_code': '0', 'data': serializer.data}
    return HttpResponse(json.dumps(resp), status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def createBooking(request):

    userid = request.POST.get('userid', 1)
    serviceid = request.POST.get('serviceid', 1)
    bookingaddress = request.POST.get('bookingaddress', '')
    bookingdate = request.POST.get('bookingdate', '')

    bookings = Booking.objects.filter(userid=userid, bookingdate=bookingdate)
    if bookings.count() > 0:
        resp_er = {'result_code': '101'}
        return HttpResponse(json.dumps(resp_er))
   
    booking = Booking()
    booking.userid = userid
    booking.serviceid = serviceid
    booking.bookingaddress = bookingaddress
    booking.bookingdate = bookingdate

    booking.save()

    resp = {'result_code': '0'}
    return HttpResponse(json.dumps(resp), status = HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny,))
def getBooking(request):

    userid = request.POST.get('userid', '')
    bookingdate = request.POST.get('bookingdate', '')

    bookings = Booking.objects.filter(userid=userid, bookingdate__contains=bookingdate).order_by('id')
    serializer = bookingSerializer(bookings, many=True)
    resp = {'result_code': '0', 'data': serializer.data}
    return HttpResponse(json.dumps(resp), status=HTTP_200_OK)



