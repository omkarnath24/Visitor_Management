from rest_framework import serializers
from vms.models import Visitor, Visitee, Visit, Gate
from django.contrib.auth.models import User


class VisitorSerializer(serializers.Serializer):
    visitorid = serializers.IntegerField()
    fullname = serializers.CharField(max_length=50)
    dateofbirth = serializers.DateField()
    address = serializers.CharField(max_length=200)
    contactno = serializers.IntegerField()
    gender = serializers.CharField(max_length=10)
    person = serializers.FileField()
    personid = serializers.IntegerField()

    def create(self, validated_data):
        return Visitor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.visitorid = validated_data.get('visitorid', instance.visitorid)
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.dateofbirth = validated_data.get('dateofbirth', instance.dateofbirth)
        instance.address = validated_data.get('address', instance.address)
        instance.contactno = validated_data.get('contactno', instance.contactno)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.person = validated_data.get('person', instance.person)
        instance.personid = validated_data.get('personid', instance.personid)
        instance.save()
        return instance


class VisiteeSerializer(serializers.Serializer):
    visiteeid = serializers.IntegerField()
    visiteeflatno = serializers.CharField(max_length=20)
    visiteename = serializers.CharField(max_length=50)
    visiteecontact = serializers.IntegerField()

    def create(self, validated_data):
        return Visitee.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.visiteeid = validated_data.get('visiteeid', instance.visiteeid)
        instance.visiteeflatno = validated_data.get('visiteeflatno', instance.visiteeflatno)
        instance.visiteename = validated_data.get('visiteename', instance.visiteename)
        instance.visiteecontact = validated_data.get('visiteecontact', instance.visiteecontact)
        instance.save()
        return instance


class VisiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        depth = 1
        fields = ['visitid', 'visitorid', 'visiteeid', 'purpose', 'vehicleno', 'checkin', 'checkout']


class GateSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    uname = serializers.CharField(max_length=50)
    pswrd = serializers.CharField(max_length=50)
    contno = serializers.IntegerField()

    def create(self, validated_data):
        return Gate.objects.create(**validated_data)


class LoginDetailSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    uname = serializers.CharField(max_length=50)
    pswrd = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Gate.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    uname = serializers.CharField(max_length=50)
    pswrd = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Gate.objects.create(**validated_data)


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class SearchSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Visitor.objects.create(**validated_data)
