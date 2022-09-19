from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import User, Bar, Stock, Reference, Order


class RegisterSerializer(ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], role="Barman")
        user.set_password(validated_data['password'])
        user.save()
        return user


class BarListSerializer(ModelSerializer):
    class Meta:
        model = Bar
        fields = ['id', 'name']


class StockListSerializer(ModelSerializer):
    # reference = serializers.CharField(source="reference.name")

    class Meta:
        model = Stock
        fields = ['reference', 'stock', 'comptoir']

    def update(self, instance, validated_data):
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()
        return instance


class StockDetailSerializer(ModelSerializer):
    ref = serializers.CharField(source="reference.ref")
    name = serializers.ReadOnlyField(source="reference.name")
    description = serializers.ReadOnlyField(source="reference.description")

    class Meta:
        model = Stock
        fields = ['ref', 'name', 'description', 'stock']


class ReferenceListSerializer(ModelSerializer):
    class Meta:
        model = Reference
        fields = ['ref', 'name', 'description']


class MenuListSerializer(ModelSerializer):
    # availability = serializers.ReadOnlyField(source="stock_reference__stock")
    ref_list = Reference.objects.filter(stock_reference__stock=0)
    ref = serializers.ReadOnlyField(source="reference.ref")

    class Meta:
        model = Reference
        fields = ['ref', 'name', 'description', 'availability']

        # print(fields[3].value)
