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
        account = request.GET.get('account')
        pk = account.lstrip('0')
        command = request.GET.get('command')
        txn_id = request.GET.get('txn_id')
        sum = request.GET.get('sum')
        dict = {}
        if command == 'check':
            try:
                order = Order.objects.get(pk=pk)
                if order.status:
                    result = 5
                    dict = {"result": result}
                else:
                    result = 0
                    price = 0
                    for i in order.products.all():
                        price += i.price
                    dict = {"result": result, "sum": price}
            except Order.DoesNotExist:
                result = 5
                dict = {"result": result}
        if command == 'pay':
            try:
                order = Order.objects.get(pk=pk)
            except Order.DoesNotExist:
                order = None
            if order and order.status == None:
                result = 0
                payment = TerminalPayment.objects.create(order=order, payed=sum)
                payment.save()
                dict = {"txn_id": txn_id, "result": result, "sum": sum}
                self.change_status(order)
            else:
                result = 5
                dict = {"result": result}
        return Response(dict, content_type='application/xml')

    def change_status(self, order):
        payments = TerminalPayment.objects.filter(order=order)
        sum_payments = 0
        for i in payments:
            sum_payments += i.payed
        price = 0
        for i in order.products.all():
            price += i.price
        if sum_payments >= price:
            order.status = 'Оплачено'
            order.save()
