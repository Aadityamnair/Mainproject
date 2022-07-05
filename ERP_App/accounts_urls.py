from django.urls import path

from ERP_App.accounts_views import IndexView, Purchase_details, Purchase_view

urlpatterns = [

    path('',IndexView.as_view()),
    path('Purchase_details',Purchase_details.as_view()),
    path('Purchase_view',Purchase_view.as_view())

]
def urls():
    return urlpatterns, 'employee','employee'