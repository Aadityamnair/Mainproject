from django.shortcuts import redirect
from django.views.generic import TemplateView

from ERP_App.models import Purchase


class IndexView(TemplateView):
    template_name = 'accounts/accounts_index.html'


class Purchase_details(TemplateView):
    template_name ='accounts/purchase.html'


    def post(self, request,*args,**kwargs):
        name = request.POST['name']

        price = request.POST['price']
        vender= request.POST['vender']
        date = request.POST['date']

        se = Purchase()
        se.name = name
        se.vendor=vender
        se.price = price
        se.date=date

        se.save()

        return redirect(request.META['HTTP_REFERER'], {'message': "product successfully added "})

class Purchase_view(TemplateView):
    template_name = 'accounts/purchase_view.html'

    def get_context_data(self, **kwargs):

        context = super(Purchase_view,self).get_context_data(**kwargs)

        view_pr = Purchase.objects.all()

        context['view_pr'] = view_pr
        return context

