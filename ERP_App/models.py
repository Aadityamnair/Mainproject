from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserType(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    type = models.CharField(max_length=50)

class Hr_Reg(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    con_password=models.CharField(max_length=200,null=True)
    type=models.CharField(max_length=200,null=True)

class Accounts_Reg(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    con_password=models.CharField(max_length=200,null=True)
    type=models.CharField(max_length=200,null=True)

class desig_category(models.Model):
    name=models.CharField(max_length=200,unique=True)

class Accounts_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    name=models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    dateofbirth = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='images/', null=True)
    salary=models.CharField(max_length=200, null=True)

class hr_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    name=models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    dateofbirth = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='images/', null=True)
    salary=models.CharField(max_length=200, null=True)

class employee_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    name=models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    dateofbirth = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True)

    image = models.ImageField(upload_to='images/', null=True)
    salary=models.CharField(max_length=200, null=True)

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    con_passwod=models.CharField(max_length=200,null=True)
    type=models.CharField(max_length=200,null=True)





class Project_Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    name = models.CharField(max_length=200, null=True)
    deadline_date=models.CharField(max_length=200,null=True)
    description=models.CharField(max_length=200,null=True)
    client=models.CharField(max_length=200,null=True)
    price=models.CharField(max_length=200,null=True)
    status=models.CharField(max_length=200,null=True)
    blockchain_status = models.CharField(max_length=100, default='not active')
    blockchain_count = models.IntegerField(default=0)
    blockchain_entry_count = models.IntegerField(default=0)

class blockchain_ledger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project_Details, on_delete=models.CASCADE,null=True)

    date = models.DateField(null=False, blank=False, auto_now=True)
    time = models.DateTimeField(max_length=100, auto_now=True)
    Remark = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=100,null=True)
    blockchain_count = models.IntegerField(default=0)
    blockchain_entry_count = models.IntegerField(default=0)
    last_status = models.CharField(max_length=100,default='not active')

    remarks = models.CharField(max_length=200, null=True)
    count = models.IntegerField(null=True)



class Add_task(models.Model):
    project = models.ForeignKey(Project_Details, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200, null=True)
    project_mng= models.CharField(max_length=200, null=True)
    lead= models.CharField(max_length=200, null=True)
    eng1 = models.CharField(max_length=200, null=True)
    eng2 = models.CharField(max_length=200, null=True)
    eng3 = models.CharField(max_length=200, null=True)
    eng4 = models.CharField(max_length=200, null=True)
    eng5 = models.CharField(max_length=200, null=True)


class Purchase(models.Model):
    name = models.CharField(max_length=200, null=True)
    date=models.CharField(max_length=200,null=True)
    vendor=models.CharField(max_length=200,null=True)
    price=models.CharField(max_length=200,null=True)


class Blockchain_admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    employee=models.ForeignKey(employee_details,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=200,null=True)
    department = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, null=True)
    status=models.CharField(max_length=200,null=True)
    key=models.CharField(max_length=200,null=True)
    key2=models.CharField(max_length=200,null=True,default="null")



class Leave(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    employee = models.ForeignKey(employee_details, on_delete=models.CASCADE)
    leavetype = models.CharField(max_length=100,null=True)
    fromdate = models.CharField(max_length=100,null=True)
    noday = models.IntegerField(max_length=100,null=True)
    enddate = models.CharField(max_length=100,null=True)
    leaveperiod = models.CharField(max_length=100,null=True)
    reason = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=100, null=True)

class Blockchain_ledger_encripted(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_name = models.CharField(max_length=100, null=True)
    project = models.ForeignKey(Project_Details, on_delete=models.CASCADE, null=True)
    datetime = models.DateTimeField(auto_now=True)
    Remark = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    blockchain_count = models.CharField(max_length=100,default=0)
    blockchain_entry_count = models.CharField(max_length=100,default=0)
    last_status = models.CharField(max_length=100, default='not active')
    remarks = models.CharField(max_length=200, null=True)
    count = models.IntegerField(null=True)