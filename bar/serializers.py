from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import User, Bar, Stock, Reference, Order, OrderItems


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
    availability = serializers.SerializerMethodField()

    @staticmethod
    def get_availability(ref):

        refs_stock = Stock.objects.filter(reference=ref)
        refs_list_outofstock = Stock.objects.filter(reference=ref, stock=0)

        if len(refs_stock) == len(refs_list_outofstock):
            ref.availability = 'outofstock'

        return ref.availability

    class Meta:
        model = Reference
        fields = ['ref', 'name', 'description', 'availability']


class OrderItemsSerializer(ModelSerializer):

    class Meta:
        model = OrderItems
        fields = ['item']


class OrderSerializer(ModelSerializer):
    items = serializers.SerializerMethodField()

    @staticmethod
    def get_items(order):

        list_orderitems = OrderItems.objects.filter(order=order)

        list_items = []

        for orderitem in list_orderitems:
            item = Reference.objects.get(name=orderitem.item)
            ref = item.ref
            name = item.name
            description = item.description
            list_items.append({"ref": ref,
                               "name": name,
                               "description": description
                               })
        return list_items

    class Meta:
        model = Order
        fields = ['id', 'items']


class RankingAllSerializer(ModelSerializer):

    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    bars = serializers.SerializerMethodField()

    @staticmethod
    def get_name(bar):
        return "all_stock"

    @staticmethod
    def get_description(bar):
        return "Liste des comptoirs qui ont toutes les références en stock"

    @staticmethod
    def get_bars(bar):
        bars = Bar.objects.all()
        references = Reference.objects.all()
        all_stock = []
        for bar in bars:
            references_available = []
            for reference in references:
                stock = Stock.objects.get(comptoir=bar, reference=reference)
                if stock.stock != 0:
                    references_available.append(reference)
            if len(references_available) == len(references):
                all_stock.append(bar.id)
        return all_stock

    class Meta:
        model = Bar
        fields = ['name', 'description', 'bars']


class RankingMissSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    bars = serializers.SerializerMethodField()

    @staticmethod
    def get_name(bar):
        return "miss_at_least_one"

    @staticmethod
    def get_description(bar):
        return "Liste de comptoirs qui ont au moins une référence épuisée"

    @staticmethod
    def get_bars(bar):
        miss_at_least_one = []
        bars = Bar.objects.all()
        references = Reference.objects.all()
        for bar in bars:
            references_out = []
            for reference in references:
                stock = Stock.objects.get(comptoir=bar, reference=reference)
                if stock.stock == 0:
                    references_out.append(reference)
            if references_out:
                miss_at_least_one.append(bar.id)
        return miss_at_least_one

    class Meta:
        model = Bar
        fields = ['name', 'description', 'bars']
