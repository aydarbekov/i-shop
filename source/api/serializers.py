from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=120)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    products = serializers.CharField()
