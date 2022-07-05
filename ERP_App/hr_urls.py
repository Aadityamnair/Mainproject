from django.urls import path

from ERP_App.hr_views import IndexView, Add_Project, Schedule_task, Employee_Reg, Add_Employee, View_employee, \
    Leave_Request, AcceptLeave, RejectLeave, EmployeeEdit

urlpatterns = [

    path('',IndexView.as_view()),
    path('employee',Employee_Reg.as_view()),
    path('Add_Employee',Add_Employee.as_view()),
    path('Add_Project',Add_Project.as_view()),
    path('Add_task',Schedule_task.as_view()),
    path('View_employee',View_employee.as_view()),
    path('Leave_Request',Leave_Request.as_view()),
    path('approve',AcceptLeave.as_view()),
    path('reject',RejectLeave.as_view()),
    path('employee_edit',EmployeeEdit.as_view())

]
def urls():
    return urlpatterns, 'hr','hr'