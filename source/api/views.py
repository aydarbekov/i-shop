from django.shortcuts import render

# Create your views here.
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Order
from .serializers import OrderSerializer


class OrderView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        account = request.GET.get('\naccount')
        print(account, "THIS IS DATA")
        command = request.GET.get('command')
        print(command, "THIS IS COMMANDD")
        # return Response({"articles": serializer.data})
        data = serializers.serialize('xml', Order.objects.filter(pk=2), fields=('first_name', 'user'))
        # return Response({"orders": serializer.data})
        return Response({data})