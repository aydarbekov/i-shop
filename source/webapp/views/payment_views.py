from django.views.generic.base import TemplateView


class PaymentView(TemplateView):
    template_name = 'payment.html'