from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from ERP_App.models import UserType


class IndexView(TemplateView):
    template_name = 'index.html'





class Login(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            if user.last_name == '1':
                if user.is_superuser:
                    return redirect('/admin')
                elif UserType.objects.get(user_id=user.id).type == "hr":
                    return redirect('/hr')
                elif UserType.objects.get(user_id=user.id).type == "employee":
                    return redirect('/employee')
                elif UserType.objects.get(user_id=user.id).type == "accounts":
                    return redirect('/accounts')

            else:
                return render(request, 'login.html', {'message': " User Account Not Authenticated"})


        else:
            return render(request, 'login.html', {'message': "Invalid Username or Password"})