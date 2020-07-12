from django.shortcuts import render

# Create your views here.
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Order, TerminalPayment
from .serializers import OrderSerializer
from rest_framework_xml.renderers import XMLRenderer


class ApiXmlRenderer(XMLRenderer):
    root_tag_name = "response"


class OrderView(APIView):
    renderer_classes = [ApiXmlRenderer]

    def get(self, request):
        orders = Order.objects.all()
        account = request.GET.get('account')
        pk = account.lstrip('0')
        command = request.GET.get('command')
        order = None
        result = None
        txn_id = request.GET.get('txn_id')
        sum = request.GET.get('sum')
        if command == 'check':
            try:
                order = Order.objects.get(pk=pk)
                result = 0
            except Order.DoesNotExist:
                order = None
                result = 5
            print(command, "THIS IS COMMANDD")
            print(order, "THIS IS ORDER")
            print(result, "THIS IS RESULT")
        if command == 'pay':
            try:
                order = Order.objects.get(pk=pk)
            except Order.DoesNotExist:
                order = None
            if order:
                result = 0
                payment = TerminalPayment.objects.create(order=order, payed=sum)
                payment.save()
            else:
                result = 5
            print(command, "THIS IS COMMANDD")
            print(order, "THIS IS ORDER")
            print(result, "THIS IS RESULT")

        print(sum)
        price = 0
        # for i in order.products.all():
        #     price += i.price
        # print(price, "THIS IS PRICE")
        # text = '<?xml version="1.0" encoding="utf-8"?><response><result></result><sum>1500</sum><comment>OK</comment></response>'
        dict = {"result":result, "sum":price}
        return Response(dict, content_type='application/xml')
