from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
import string
import random

from ERP_App.models import Hr_Reg, UserType, hr_details, Accounts_Reg, Accounts_details, Blockchain_admin, \
    employee_details, blockchain_ledger, Project_Details, Add_task


class IndexView(TemplateView):
    template_name = 'admin/admin_index.html'

class Registration(TemplateView):
    template_name = 'admin/registration.html'

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        email = request.POST['email']
        type=request.POST['type']
        password = request.POST['password']
        # designation=request.POST['designation']
        # dateofbirth=request.POST['dateofbirth']
        # address=request.POST['address']
        con_password = request.POST['con_password']

        # address = request.POST['address']
        if password == con_password:

            if User.objects.filter(email=email):
                print('pass')
                return render(request, 'admin/registration.html', {'message': "already added the email"})

            else:
                user = User.objects._create_user(username=email, password=password, email=email, first_name=name,
                                                 is_staff='0', last_name='1')
                user.save()
                hr= Hr_Reg()
                hr.user = user
                hr.type=type
                # hr.address= address
                # hr.designation=designation
                # hr.dateofbirth=dateofbirth
                hr.con_password = con_password
                hr.save()
                usertype = UserType()

                usertype.user = user
                usertype.type = "hr"
                usertype.save()
                return render(request, 'admin/hr_details.html', {'message': "successfully added"})
        else:
            return render(request, 'admin/registration.html', {'message': "password didn't match"})

class Accounts_Registration(TemplateView):
    template_name = 'admin/accounts_registration.html'

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        email = request.POST['email']
        type=request.POST['type']
        password = request.POST['password']
        # designation=request.POST['designation']
        # dateofbirth=request.POST['dateofbirth']
        # address=request.POST['address']
        con_password = request.POST['con_password']

        # address = request.POST['address']
        if password == con_password:

            if User.objects.filter(email=email):
                print('pass')
                return render(request, 'admin/accounts_registration.html', {'message': "already added the email"})

            else:
                user = User.objects._create_user(username=email, password=password, email=email, first_name=name,
                                                 is_staff='0', last_name='1')
                user.save()
                hr= Accounts_Reg()
                hr.user = user
                hr.type=type
                # hr.address= address
                # hr.designation=designation
                # hr.dateofbirth=dateofbirth
                hr.con_password = con_password
                hr.save()
                usertype = UserType()

                usertype.user = user
                usertype.type = "accounts"
                usertype.save()
                return render(request, 'admin/accounts_registration.html', {'message': "successfully added"})
        else:
            return render(request, 'admin/accounts_registration.html', {'message': "password didn't match"})

class Hr_details(TemplateView):
    template_name ='admin/hr_details.html'

    def get_context_data(self, **kwargs):

        context = super(Hr_details, self).get_context_data(**kwargs)
        hr = Hr_Reg.objects.filter(type='hr')
        context['hr'] = hr
        return context


    def post(self, request,*args,**kwargs):
        name = request.POST['name']

        image = request.FILES['image']
        fii = FileSystemStorage()
        filesss = fii.save(image.name, image)
        dateofbirth = request.POST['dateofbirth']
        address= request.POST['address']
        salary = request.POST['salary']
        designation = request.POST['designation']

        se = hr_details()
        se.user_id=name
        se.designation=designation
        se.salary = salary
        se.image=filesss
        se.dateofbirth = dateofbirth
        se.address=address
        se.save()

        return redirect(request.META['HTTP_REFERER'], {'message': "product successfully added "})


class accounts_details(TemplateView):
    template_name ='admin/accounts_details.html'

    def get_context_data(self, **kwargs):

        context = super(accounts_details, self).get_context_data(**kwargs)
        accounts = Accounts_Reg.objects.filter(type='accounts')
        context['accounts'] = accounts
        return context


    def post(self, request,*args,**kwargs):
        name = request.POST['name']

        image = request.FILES['image']
        fii = FileSystemStorage()
        filesss = fii.save(image.name, image)
        dateofbirth = request.POST['dateofbirth']
        address= request.POST['address']
        salary = request.POST['salary']
        designation = request.POST['designation']


        se = Accounts_details()
        se.user_id=name
        se.designation=designation
        se.salary = salary
        se.image=filesss
        se.dateofbirth = dateofbirth
        se.address=address
        se.save()

        return redirect(request.META['HTTP_REFERER'], {'message': "product successfully added "})


class Blockchain_admin_add(TemplateView):
    template_name = 'admin/employees.html'

    def get_context_data(self, **kwargs):

        context = super(Blockchain_admin_add, self).get_context_data(**kwargs)
        all = employee_details.objects.all()
        context['all'] = all
        return context


class Profile_details(TemplateView):
    template_name = 'admin/profile_details.html'

    def get_context_data(self, **kwargs):
        id = self.request.GET['id']

        context = super(Profile_details, self).get_context_data(**kwargs)

        single_view = employee_details.objects.get(id=id)

        context['single_view'] = single_view

        return context

    def post(self, request, *args, **kwargs):
        S = 16

        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
        count = len(ran)
        range = ran[0:count:4]
        print(range)
        ascii_values = []
        for i in range:
            print(i)
            ascii_values.append(ord(i))
        values_sum = sum(ascii_values)
        print(values_sum)
        print(ascii_values)
        print("The randomly generated string is : " + str(ran))




        name = request.POST['name']
        dept=request.POST['dept']
        desig=request.POST['desig']
        user=request.POST['user']
        employee=request.POST['employee']
        if Blockchain_admin.objects.filter(user_id=user):
            print("fvvfsff")
            return render(request, 'admin/admin_index.html', {'message': "Already Added"})
        else:

            se=Blockchain_admin()
            se.name=name
            se.department=dept
            se.designation=desig
            se.user_id=user
            se.employee_id=employee
            se.key=ran
            se.key2=values_sum
            se.status='blockchain_admin'

            se.save()


            return render(request, 'admin/admin_index.html', {'message': "Blockchain admin added successfully"})

class View_Projects(TemplateView):
    template_name = 'admin/view_projects.html'

    def get_context_data(self, **kwargs):
        context = super(View_Projects,self).get_context_data(**kwargs)
        cri = Add_task.objects.all()

        context['cri'] = cri

        return context

    def post(self, request, *args, **kwargs):
        # template = loader.get_template('user/store.html')
        search = self.request.POST['search']
        cri = Add_task.objects.filter(project_name__icontains=search)
        # return HttpResponse(template.render({"train": train}))
        return render(request,'admin/view_projects.html',{'cri':cri})




