from rest_framework.serializers import ModelSerializer

from .models import Table, Order


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


class TableSerializer(ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"





