from django.shortcuts import render

# Create your views here.
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Order, TerminalPayment
from .serializers import OrderSerializer
from rest_framework_xml.renderers import XMLRenderer
from main.settings import API_TOKEN


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
        token = request.GET.get('token')
        dict = {}
        if token == API_TOKEN:
            if command == 'check':
                dict = self.check_api(pk)
                return Response(dict, content_type='application/xml')
            if command == 'pay':
                dict = self.pay_api(pk, txn_id, sum)
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

    def get_payment(self, txn_id):
        try:
            payment = TerminalPayment.objects.get(txn_id=txn_id)
            payment = False
        except TerminalPayment.DoesNotExist:
            payment = True
        return payment

    def get_sum(self, order):
        payments = TerminalPayment.objects.filter(order=order)
        sum_payments = 0
        for i in payments:
            sum_payments += i.payed
        price = 0
        for i in order.products.all():
            price += i.price
        sum = price-sum_payments
        return sum

    def check_api(self, pk):
        try:
            order = Order.objects.get(pk=pk)
            if order.status:
                result = 5
                dict = {"result": result}
            else:
                result = 0
                sum = self.get_sum(order)
                dict = {"result": result, "sum": sum}
        except Order.DoesNotExist:
            result = 5
            dict = {"result": result}
        return dict

    def pay_api(self, pk, txn_id, sum):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            order = None
        if order and order.status == None and self.get_payment(txn_id):
            result = 0
            payment = TerminalPayment.objects.create(order=order, payed=sum, txn_id=txn_id)
            payment.save()
            dict = {"txn_id": txn_id, "result": result, "sum": sum}
            self.change_status(order)
        else:
            result = 5
            dict = {"result": result}
        return dict

