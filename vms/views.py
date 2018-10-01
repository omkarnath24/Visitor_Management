# from django.shortcuts import render
from django.core import serializers
from rest_framework import generics, status
from rest_framework.response import Response
from vms.models import Visitor, Visitee, Visit, Gate
from vms.serializers import (VisitorSerializer, VisiteeSerializer, VisiSerializer, GateSerializer,
                             LoginDetailSerializer, LoginSerializer, UserSerializer, SearchSerializer
                             )
from django.conf import settings
from Visitor_Management import settings
import jwt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import base64
import datetime, os
from django.http.response import HttpResponse
import uuid


class JwtToken(object):
    def JwtTokenEncode(self, uid):
        print(uid)
        token = jwt.encode({'uid': uid}, settings.SECRET_KEY, algorithm='HS256')
        return token

    def JwtTokenDecode(self, token):
        pay_load = jwt.decode(token, settings.SECRET_KEY)
        return pay_load


class Basic(generics.ListAPIView):
    def list(self, request):
        return Response({'Message': 'Ready To Use API TESTING', 'Status': 'True'}, status=status.HTTP_200_OK)


class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request):
        uname = request.data['uname']
        pswrd = request.data['pswrd']
        uid = User.objects.get(username=uname)

        if (uid.check_password(pswrd)):
            print('AUTHORIZED ACCESS')
            token = JwtToken.JwtTokenEncode(self, uid.id)
            # print(token)

            return Response({'token': token, 'Message': 'AUTHORIZED ACCESS', 'Status': True},
                            status=status.HTTP_202_ACCEPTED)
        else:
            print('UNAUTHORIZED ACCESS')
            return Response({'Message': 'UNAUTHORIZED ACCESS', 'Status': 'False'}, status=status.HTTP_401_UNAUTHORIZED)


class LoginDetails(generics.CreateAPIView):
    serializer_class = LoginDetailSerializer

    def create(self, request):
        firstname = request.data['first']
        lastname = request.data['last']
        uname = request.data['uname']
        pswrd = make_password(request.data['pswrd'], salt=None)

        User(first_name=firstname, last_name=lastname, username=uname, password=pswrd).save()
        return Response({'Message': 'New User Created', 'Status': 'True'}, status=status.HTTP_200_OK)


class VisitorCreate(generics.ListCreateAPIView):
    serializer_class = VisitorSerializer

    def list(self, request):
        jwtObj = JwtToken()
        # print(request.META.get('HTTP_AUTHORIZATION'))
        pay_load = jwtObj.JwtTokenDecode(request.META.get('HTTP_AUTHORIZATION'))
        user_id = User.objects.get(id=pay_load['uid'])
        print("USERID:", pay_load)
        print("USERNAME:", user_id)
        data = serializers.serialize('json', Visitor.objects.all())
        return Response({'visitor': data}, status=status.HTTP_200_OK)

    def create(self, request):
        jwtObj = JwtToken()
        # print(request.META.get('HTTP_AUTHORIZATION'))
        pay_load = jwtObj.JwtTokenDecode(request.META.get('HTTP_AUTHORIZATION'))
        user_id = User.objects.get(id=pay_load['uid'])
        print("VISITOR CREATED BY:")
        print("USERID:", pay_load)
        print("USERNAME:", user_id)

        way = os.getcwd()
        today = datetime.date.today()
        todaystr = today.isoformat()
        os.chdir(way)

        if os.path.isdir('Images'):
            os.chdir("Images")
        else:
            os.mkdir('Images')
            os.chdir("Images")

        if os.path.isdir(todaystr):
            os.chdir(todaystr)
        else:
            os.mkdir(todaystr)
            os.chdir(todaystr)

        fullname = request.data['fullname']
        dateofbirth = request.data['dateofbirth']
        address = request.data['address']
        contactno = request.data['contactno']
        gender = request.data['gender']
        person = request.data['person']
        img = base64.b64decode(person)

        if os.path.isdir(contactno):
            os.chdir(contactno)

        else:
            os.mkdir(contactno)
            os.chdir(contactno)

        dr = os.getcwd()

        prsn = dr + '/' + contactno + '.jpg'
        with open(prsn, 'wb') as f:
            f.write(img)
        personid = request.data['personid']
        imgid = base64.b64decode(personid)
        prsnid = dr + '/' + contactno + '_id.jpg'
        with open(prsnid, 'wb') as f:
            f.write(imgid)

        vehicle = request.data['vehicleno']
        imgveh = base64.b64decode(vehicle)
        prsnveh = dr + '/' + contactno + '_veh.jpg'
        with open(prsnveh, 'wb') as f:
            f.write(imgveh)

        visname = request.data['visname']
        # visdate = request.data['visitdate']
        reason = request.data['reason']
        checkin = request.data['checkin']
        i = Visitor(fullname=fullname, dateofbirth=dateofbirth, address=address, contactno=contactno, gender=gender,
                    person=prsn, personid=prsnid)
        i.save()
        vid = Visitee.objects.get(visiteename=visname)

        Visit(visitorid=i, visiteeid=vid, vehicleno=prsnveh, purpose=reason, checkin=checkin).save()
        os.chdir(way)
        return Response({'Message': 'New Visitor Created', 'Status': 'True'}, status=status.HTTP_201_CREATED)


class VisitorView(generics.ListAPIView):
    serializer_class = VisitorSerializer

    def get_queryset(self):
        return Visitor.objects.all()


class VisiteeList(generics.ListAPIView):
    serializer_class = VisiteeSerializer

    def get_queryset(self):
        return Visitee.objects.all()


class VisitHistory(generics.ListCreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisiSerializer


class Check(generics.UpdateAPIView):
    def put(self, request):
        jwtObj = JwtToken()
        pay_load = jwtObj.JwtTokenDecode(request.META.get('HTTP_AUTHORIZATION'))
        user_id = User.objects.get(id=pay_load['uid'])
        print("USERID:", pay_load)
        print("USERNAME:", user_id)
        visitid = request.data['visitid']
        checkout = request.data['checkout']
        # checkout=request.data['checkout']
        Visit.objects.filter(visitid=visitid).update(checkout=checkout)
        return Response({'Message': 'Checkout Successful', 'Status': 'True'}, status=status.HTTP_201_CREATED)


class Search(generics.CreateAPIView):
    serializer_class = SearchSerializer

    def create(self, request):
        jwtObj = JwtToken()
        pay_load = jwtObj.JwtTokenDecode(request.META.get('HTTP_AUTHORIZATION'))
        user_id = User.objects.get(id=pay_load['uid'])
        print("USERID:", pay_load)
        print("USERNAME:", user_id)
        vcnt = request.data['contactno']

        if (Visitor.objects.filter(contactno=vcnt).exists()):
            vt = Visitor.objects.get(contactno=vcnt)
            return HttpResponse(vt, status=status.HTTP_202_ACCEPTED)
        else:
            print("Visitor Not Found")
            return Response({'Message': 'Visitor Not Found', 'Status': 'False'}, status=status.HTTP_404_NOT_FOUND)


class Update(generics.CreateAPIView):
    def create(self, request):
        jwtObj = JwtToken()
        pay_load = jwtObj.JwtTokenDecode(request.META.get('HTTP_AUTHORIZATION'))
        user_id = User.objects.get(id=pay_load['uid'])
        print("USERID:", pay_load)
        print("USERNAME:", user_id)

        today = datetime.date.today()
        todaystr = today.isoformat()
        way = os.getcwd()
        os.chdir(way)

        if os.path.isdir('ExistingVisitor'):
            os.chdir("ExistingVisitor")
        else:
            os.mkdir('ExistingVisitor')
            os.chdir("ExistingVisitor")

        if os.path.isdir(todaystr):
            os.chdir(todaystr)
        else:
            os.mkdir(todaystr)
            os.chdir(todaystr)

        phone = request.data['phone']
        vname = request.data['vname']
        purpose = request.data['purpose']
        checkin = request.data['checkin']

        if os.path.isdir(phone):
            os.chdir(phone)

        else:
            os.mkdir(phone)
            os.chdir(phone)

        dr = os.getcwd()
        vehi = request.data['vehicleno']
        imgveh = base64.b64decode(vehi)
        vehi = dr + '/' + phone + '_veh.jpg'
        with open(vehi, 'wb') as f:
            f.write(imgveh)

        vts = Visitor.objects.get(contactno=phone)
        vst = Visitee.objects.get(visiteename=vname)
        Visit(purpose=purpose, checkin=checkin, vehicleno=vehi, visitorid=vts, visiteeid=vst).save()
        os.chdir(way)
        return Response({'Message': 'Update Successful', 'Status': 'True'}, status=status.HTTP_201_CREATED)


class GateView(generics.ListCreateAPIView):
    serializer_class = GateSerializer

    def list(self, request):
        jwtObj = JwtToken()
        pay_load = jwtObj.JwtTokenDecode(request.META.get('HTTP_AUTHORIZATION'))
        user_id = User.objects.get(id=pay_load['uid'])
        print("USERID:", pay_load)
        print("USERNAME:", user_id)
        data = serializers.serialize('json', Gate.objects.all())
        return Response({'gate': data}, status=status.HTTP_200_OK)

    def create(self, request):
        uname = request.data['uname']
        pswrd = request.data['pswrd']
        contno = request.data['contno']
        g = Gate(uname=uname, pswrd=pswrd, contno=contno)
        g.save()
        return Response(status=status.HTTP_200_OK)


class GateList(generics.ListAPIView):
    serializer_class = GateSerializer

    def get_queryset(self):
        return Gate.objects.all()


class UserDetail(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()