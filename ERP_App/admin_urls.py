from django.urls import path

from ERP_App.admin_views import IndexView, Registration, Hr_details, Accounts_Registration, accounts_details, \
    Blockchain_admin, Profile_details, Blockchain_admin_add, View_Projects

urlpatterns = [

    path('',IndexView.as_view()),
    path('reg', Registration.as_view()),
    path('Hr_details',Hr_details.as_view()),
    path('accounts',Accounts_Registration.as_view()),
    path('accounts_details',accounts_details.as_view()),
    path('Blockchain_admin',Blockchain_admin_add.as_view()),
    path('Profile_view',Profile_details.as_view()),
    path('View_Projects',View_Projects.as_view())

]
def urls():
    return urlpatterns, 'admin','admin'