from django.urls import path

from ERP_App import employee_views
from ERP_App.employee_views import IndexView, block_chain, blockchain_emList, Admin_profile, Blockchain_admin_Login, \
    view_project, Apply_Leave, Leave_status, view_ledger_login, view_block_chain, Profile_view

urlpatterns = [

    path('',IndexView.as_view()),
    path('blockchain',block_chain.as_view()),
    path('adminlist',blockchain_emList.as_view()),
    path('profile',Admin_profile.as_view()),
    path('admin_login',Blockchain_admin_Login.as_view()),
    path('view_project',view_project.as_view()),
    path('applyleave',Apply_Leave.as_view()),
    path('Leave_status',Leave_status.as_view()),
    # path('Notification',Notification.as_view()),
    path('view_ledger_login', view_ledger_login.as_view()),
    path('get_chain', employee_views.get_chain, name="get_chain"),
    # path('mine_block', user_views.mine_block,name="mine_block"),
    path('is_valid', employee_views.is_valid, name="is_valid"),

    path('view_block_chain', view_block_chain.as_view()),
    path('Profile_view',Profile_view.as_view())

    # path('Approve',ApproveView.as_view()),
    # path('Reject',Reject.as_view())
]
def urls():
    return urlpatterns, 'employee','employee'