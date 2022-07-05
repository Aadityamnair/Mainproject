from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from ERP_App.models import UserType, Employee, Project_Details, desig_category, Add_task, employee_details, \
    blockchain_ledger, Leave


class IndexView(TemplateView):
    template_name = 'hr/hr_index.html'

class Category(TemplateView):
    template_name = 'hr/desig_categ.html'

    def post(self, request, *args, **kwargs):
        name=request.POST['name']
        categ=desig_category()
        categ.name=name
        categ.save()
        return redirect(request.META['HTTP_REFERER'],{'message':"Category Successfuly Added"})



class Employee_Reg(TemplateView):
    template_name = 'hr/employee_reg.html'
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        email = request.POST['email']
        type = request.POST['type']
        con_password=request.POST['con_password']


        # image = request.FILES['image']
        # fii = FileSystemStorage()
        # filesss = fii.save(image.name, image)
        password = request.POST['password']
        # designation=request.POST['designation']
        # dateofbirth=request.POST['dateofbirth']
        # address=request.POST['address']
        con_password = request.POST['con_password']

        # address = request.POST['address']
        if password == con_password:

            if User.objects.filter(email=email):
                print('pass')
                return render(request, 'hr/hr_index.html', {'message': "already added the email"})

            else:
                user = User.objects._create_user(username=email, password=password, email=email, first_name=name,
                                                 is_staff='0', last_name='1')
                user.save()
                em= Employee()
                em.user = user
                em.con_password = con_password
                em.type=type
                em.save()
                usertype = UserType()

                usertype.user = user
                usertype.type = "employee"
                usertype.save()
                return render(request, 'hr/hr_index.html', {'message': "successfully added"})
        else:
            return render(request, 'hr/hr_index.html', {'message': "password didn't match"})

class Add_Employee(TemplateView):
    template_name = 'hr/add_employee.html'

    def get_context_data(self, **kwargs):
        context = super(Add_Employee, self).get_context_data(**kwargs)
        employee = Employee.objects.filter(type='employee')
        context['employee'] = employee
        return context
    def post(self, request,*args,**kwargs):
        name = request.POST['name']

        image = request.FILES['image']
        fii = FileSystemStorage()
        filesss = fii.save(image.name, image)
        dateofbirth = request.POST['dateofbirth']
        address= request.POST['address']
        salary = request.POST['salary']
        department=request.POST['department']
        designation = request.POST['designation']


        se = employee_details()

        se.user_id=name
        se.department=department
        se.designation=designation
        se.salary = salary
        se.image=filesss
        se.dateofbirth = dateofbirth
        se.address=address
        se.save()

        return render(request, 'hr/hr_index.html', {'message': "Details added"})


class Add_Project(TemplateView):
    template_name ='hr/project_details.html'


    def post(self, request,*args,**kwargs):
        user = User.objects.get(id=self.request.user.id)

        name = request.POST['name']

        price = request.POST['price']
        desc = request.POST['desc']
        client= request.POST['client']
        date = request.POST['date']


        s1 = Project_Details()
        s1.name = name
        s1.user=user
        s1.description = desc
        s1.client = client
        s1.price = price
        s1.deadline_date = date
        s1.status='null'
        s1.save()


        return render(request, 'hr/project_details.html', {'message': "Project Added"})


class Schedule_task(TemplateView):
    template_name = 'hr/add_task.html'

    def get_context_data(self, **kwargs):
        context = super(Schedule_task, self).get_context_data(**kwargs)
        category = Project_Details.objects.filter(blockchain_status='active')
        manager=employee_details.objects.filter(designation='Project Manager')
        lead=employee_details.objects.filter(designation='Team Lead')
        soft=employee_details.objects.filter(designation='Software Engineer')
        juni=employee_details.objects.filter(designation='Junior software Engineer')



        context['soft'] = soft
        context['juni'] = juni
        context['category'] = category

        context['lead'] = lead

        context['manager']=manager
        return context

    def post(self, request, *args, **kwargs):
        project_name = request.POST['project_name']

        project_mng = request.POST['project_mng']
        lead =  request.POST['lead']
        eng1 = request.POST['eng1']
        eng2 = request.POST['eng2']
        eng3 = request.POST['eng3']
        eng4 = request.POST['eng4']
        eng5 = request.POST['eng5']
        se = Add_task()
        se.project_id = project_name
        se.project_mng = project_mng
        se.lead = lead
        se.eng1 = eng1
        se.eng2 = eng2
        se.eng4 = eng4
        se.eng3 = eng3
        se.eng5 = eng5

        se.save()

        return render(request, 'hr/hr_index.html', {'message': "successfully added"})


class View_employee(TemplateView):
    template_name = 'hr/view_employee.html'
    def get_context_data(self, **kwargs):

        context = super(View_employee,self).get_context_data(**kwargs)

        view_pr = employee_details.objects.all()

        context['view_pr'] = view_pr
        return context

class Leave_Request(TemplateView):
    template_name = 'hr/leave_request.html'

    def get_context_data(self, **kwargs):
        context = super(Leave_Request, self).get_context_data(**kwargs)

        leave = Leave.objects.filter(status='Apply')

        context['leave'] = leave
        return context


class AcceptLeave(View):
    def dispatch(self, request, *args, **kwargs):
        id = self.request.GET['id']
        accept = Leave.objects.get(pk=id)
        accept.status = 'Accept'
        accept.save()
        return render(request, 'hr/leave_request.html', {'message': "Approve"})


class RejectLeave(View):
    def dispatch(self, request, *args, **kwargs):
        id = self.request.GET['id']
        reject = Leave.objects.get(pk=id)
        reject.status = 'Reject'
        reject.save()
        return render(request, 'hr/leave_request.html', {'message': "Reject"})

class EmployeeEdit(TemplateView):
    template_name = 'hr/edit_employee.html'

    def post(self,request,*args,**kwargs):
        id = self.request.GET['id']
        employee = employee_details.objects.get(pk=id)
        if request.POST['profile'] == "profile":
            employee.designation=request.POST['designation']
            employee.department = request.POST['department']
            employee.save()
            return render(request,'hr/view_employee.html',{'message':"Employee Profile Updated"})
        else:
            employee.salary = request.POST['salary']
            employee.save()
            return render(request,'hr/view_employee.html',{'message':"Salary Updated"})