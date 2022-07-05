import datetime
from cryptography.fernet import Fernet
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
import hashlib
import json

from ERP_App.models import Blockchain_admin, blockchain_ledger, Project_Details, employee_details, Leave, \
    Blockchain_ledger_encripted


class IndexView(TemplateView):
    template_name = 'employee/employee_index.html'


class block_chain(TemplateView):
    template_name = 'employee/block_chain.html'

class blockchain_emList(TemplateView):
    template_name = 'employee/blockchain_adminlist.html'
    def get_context_data(self, **kwargs):
        context = super(blockchain_emList, self).get_context_data(**kwargs)
        employee = Blockchain_admin.objects.all()
        context['employee'] = employee
        return context

class Admin_profile(TemplateView):
    template_name = 'employee/blockchain_em_profile.html'

    def get_context_data(self, **kwargs):
        id = self.request.GET['id']
        context = super(Admin_profile, self).get_context_data(**kwargs)
        single_view = Blockchain_admin.objects.get(id=id)
        context['single_view'] = single_view
        return context


class Blockchain_admin_Login(TemplateView):
    template_name = 'employee/blockchain_admin_login.html'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        key = request.POST['key']
        if (Blockchain_admin.objects.filter(user_id=user,key=key)):

            return render(request, 'employee/admin_page.html', {'message': " login Successfully"})

        else:
            return render(request, 'employee/employee_index.html', {'message': " invalid key"})



class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(nonce = 1, previous_hash = '0')

    def create_block(self, nonce, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'nonce': nonce,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


# Creating our Blockchain
blockchain = Blockchain()

# Mining a new block
def mine_block(request):
    if request.method == 'GET':
        previous_block = blockchain.get_previous_block()
        previous_nonce = previous_block['nonce']
        nonce = blockchain.proof_of_work(previous_nonce)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(nonce, previous_hash)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'nonce': block['nonce'],
                    'previous_hash': block['previous_hash']}
    return JsonResponse(response)

# Getting the full Blockchain
def get_chain(request):
    if request.method == 'GET':
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
    return JsonResponse(response)

# Checking if the Blockchain is valid
def is_valid(request):
    if request.method == 'GET':
        is_valid = blockchain.is_chain_valid(blockchain.chain)
        if is_valid:
            response = {'message': 'All good. The Blockchain is valid.'}
        else:
            response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return JsonResponse(response)









class view_project(TemplateView):
    template_name = 'employee/projects.html'

    def get_context_data(self, **kwargs):
        context = super(view_project, self).get_context_data(**kwargs)
        project = Project_Details.objects.all()
        context['project'] = project
        return context


    def post(self, request,*args,**kwargs):

        id=request.POST['id']
        type=request.POST['type']
        user = User.objects.get(id=self.request.user.id)

        remark=request.POST['remark']



        if Project_Details.objects.filter(id=id,status='null',blockchain_status='active',blockchain_count=3):
            print(2)
            Product = Project_Details.objects.filter(status='null')
            return render(request,'employee/projects.html',{'message':'Currently Active this project','pro':Product})
        else:
              try:
                print(3)
                if Project_Details.objects.get(id=id,status='null',blockchain_status='not active',blockchain_count=2):
                    if blockchain_ledger.objects.filter(user_id=user,project_id=id):
                        return render(request, 'employee/employee_index.html', {'message': 'already approved'})
                    else:
                        if type=="approve":
                            print(4)
                            Project = Project_Details.objects.get(id=id,status='null',blockchain_status='not active')

                            a=Project.blockchain_count
                            Project.blockchain_count=a+1
                            Project.blockchain_status='active'

                            b=Project.blockchain_entry_count
                            Project.blockchain_entry_count = b+1
                            Project.save()

                            ledger = blockchain_ledger()
                            ledger.project_id=Project.id
                            ledger.last_status = "active"

                            ledger.Remark=remark
                            ledger.status='approve'
                            ledger.blockchain_count=a+1
                            ledger.blockchain_entry_count=b+1
                            ledger.last_status='active'
                            ledger.user_id=user.id
                            ledger.save()

                            encript = Blockchain_ledger_encripted()
                            key = Fernet.generate_key()
                            fernet = Fernet(key)
                            message1 = "active"
                            meggage2 = 'approve'
                            blockchain_count_enc = "a+1"

                            blockchain_entry_count_enc = "b+1"
                            last_status_enc = 'active'

                            enc_message1 = fernet.encrypt(message1.encode())

                            enc_remark = fernet.encrypt(remark.encode())
                            enc_meggage2 = fernet.encrypt(meggage2.encode())
                            enc_blockchain_count_enc = fernet.encrypt(blockchain_count_enc.encode())
                            enc_blockchain_entry_count_enc = fernet.encrypt(blockchain_entry_count_enc.encode())
                            enc_last_status_enc = fernet.encrypt(last_status_enc.encode())

                            username = user.first_name
                            enc_username = fernet.encrypt(username.encode())
                            encript.user_name = enc_username

                            encript.project_id = Project.id
                            encript.last_status = enc_message1

                            encript.Remark = enc_remark

                            encript.status = enc_meggage2
                            encript.blockchain_count = enc_blockchain_count_enc
                            encript.blockchain_entry_count = enc_blockchain_entry_count_enc
                            encript.last_status = enc_last_status_enc
                            encript.user_id = user.id
                            encript.save()


                            # -------Blockchain----------------------
                            previous_block = blockchain.get_previous_block()
                            previous_nonce = previous_block['nonce']
                            nonce = blockchain.proof_of_work(previous_nonce)
                            previous_hash = blockchain.hash(previous_block)
                            block = blockchain.create_block(nonce, previous_hash)
                            response = {'message': 'Congratulations, you just mined a block!',
                                            'index': block['index'],
                                            'timestamp': block['timestamp'],
                                            'nonce': block['nonce'],
                                            'previous_hash': block['previous_hash']}

                            s = {'chain': blockchain.chain,
                                        'length': len(blockchain.chain)}
                            json_string = json.dumps(s)
                            print("11111111111111111111",json_string)
                            with open('json_data.json', 'w') as outfile:
                                 json.dump(json_string, outfile)
                            file1 = open('media/datas.txt', 'w')
                            file1.writelines(s)
                            file1.close()

                            return render(request,'employee/employee_index.html',{'message':'Approved Successfully'})
                        else:
                            print(5)
                            Project = Project_Details.objects.get(id=id,status='null',blockchain_status='not active')
                            a=Project.blockchain_count
                            Project.blockchain_count=a-1
                            Project.blockchain_status='reject'
                            b=Project.blockchain_entry_count
                            Project.blockchain_entry_count = b+1
                            Project.save()
                            ledger = blockchain_ledger()
                            ledger.project_id=Project.id
                            ledger.last_status = "reject"

                            ledger.Remark=remark
                            ledger.status='reject'
                            ledger.last_status='active'
                            ledger.blockchain_count=a-1
                            ledger.blockchain_entry_count=b+1
                            ledger.user_id=user.id
                            ledger.save()

                            encript = Blockchain_ledger_encripted()
                            key = Fernet.generate_key()
                            fernet = Fernet(key)
                            message1 = 'reject'
                            meggage2 = 'reject'
                            blockchain_count_enc = "a+1"

                            blockchain_entry_count_enc = "b+1"
                            last_status_enc = "reject"

                            enc_message1 = fernet.encrypt(message1.encode())

                            enc_remark = fernet.encrypt(remark.encode())
                            enc_meggage2 = fernet.encrypt(meggage2.encode())
                            enc_blockchain_count_enc = fernet.encrypt(blockchain_count_enc.encode())
                            enc_blockchain_entry_count_enc = fernet.encrypt(blockchain_entry_count_enc.encode())
                            enc_last_status_enc = fernet.encrypt(last_status_enc.encode())

                            username = user.first_name
                            enc_username = fernet.encrypt(username.encode())
                            encript.user_name = enc_username
                            encript.project_id = Project.id
                            encript.last_status = enc_message1

                            encript.Remark = enc_remark
                            encript.status = enc_meggage2
                            encript.blockchain_count = enc_blockchain_count_enc
                            encript.blockchain_entry_count = enc_blockchain_entry_count_enc
                            encript.last_status = enc_last_status_enc
                            encript.user_id = user.id

                            encript.save()
                            return render(request,'employee/employee_index.html',{'message':'Reject Successfully'})
              except:
                  if blockchain_ledger.objects.filter(user_id=user,project_id=id):
                      return render(request, 'employee/employee_index.html', {'message': 'already done'})
                  else:
                     if type=="approve":
                            print(6)
                            Project = Project_Details.objects.get(id=id,status='null',blockchain_status='not active')
                            a=Project.blockchain_count
                            Project.blockchain_count=a+1
                            b=Project.blockchain_entry_count
                            Project.blockchain_entry_count = b+1
                            Project.save()
                            ledger = blockchain_ledger()
                            ledger.project_id=Project.id

                            ledger.Remark=remark
                            ledger.status='approve'
                            ledger.blockchain_count=a+1
                            ledger.blockchain_entry_count=b+1
                            ledger.user_id=user.id
                            ledger.save()

                            encript = Blockchain_ledger_encripted()
                            key = Fernet.generate_key()
                            fernet = Fernet(key)

                            blockchain_count_enc = "a+1"

                            blockchain_entry_count_enc = "b+1"

                            status_enc = 'approve'
                            enc_remark = fernet.encrypt(remark.encode())
                            enc_status_enc = fernet.encrypt(status_enc.encode())
                            enc_blockchain_count_enc = fernet.encrypt(blockchain_count_enc.encode())
                            enc_blockchain_entry_count_enc = fernet.encrypt(blockchain_entry_count_enc.encode())
                            encript.project_id = Project.id

                            username = user.first_name
                            enc_username = fernet.encrypt(username.encode())
                            encript.user_name = enc_username
                            encript.Remark = enc_remark
                            encript.status = enc_status_enc
                            encript.blockchain_count = enc_blockchain_count_enc
                            encript.blockchain_entry_count = enc_blockchain_entry_count_enc
                            encript.user_id = user.id
                            encript.save()
                            return render(request,'employee/employee_index.html',{'message':'Approved Successfully'})

                     else:
                            print(7)
                            Project = Project_Details.objects.get(id=id,status='null',blockchain_status='not active')
                            if blockchain_ledger.objects.filter(user_id=user,project_id=id):
                                return render(request, 'employee/employee_index.html', {'message': 'already reject'})
                            else:
                                a=Project.blockchain_count
                                if a>0:
                                    print('mmmmmm')
                                    Project.blockchain_count=a-1
                                    b=Project.blockchain_entry_count
                                    Project.blockchain_entry_count = b+1
                                    Project.save()
                                    ledger = blockchain_ledger()
                                    ledger.project_id=Project.id
                                    ledger.Remark=remark
                                    ledger.status='reject'
                                    ledger.blockchain_count=a-1
                                    ledger.blockchain_entry_count=b+1
                                    ledger.user_id=user.id
                                    ledger.save()

                                    encript = Blockchain_ledger_encripted()
                                    key = Fernet.generate_key()
                                    fernet = Fernet(key)

                                    blockchain_count_enc = "a-1"

                                    blockchain_entry_count_enc = "b+1"
                                    status_enc = 'reject'
                                    enc_remark = fernet.encrypt(remark.encode())
                                    enc_status_enc = fernet.encrypt(status_enc.encode())
                                    enc_blockchain_count_enc = fernet.encrypt(blockchain_count_enc.encode())
                                    enc_blockchain_entry_count_enc = fernet.encrypt(blockchain_entry_count_enc.encode())
                                    encript.project_id = Project.id
                                    username = user.first_name
                                    enc_username = fernet.encrypt(username.encode())
                                    encript.user_name = enc_username
                                    encript.Remark = enc_remark
                                    encript.status = enc_status_enc
                                    encript.blockchain_count = enc_blockchain_count_enc
                                    encript.blockchain_entry_count = enc_blockchain_entry_count_enc
                                    encript.user_id = user.id
                                    encript.save()
                                    return render(request,'employee/employee_index.html',{'message':'Reject Successfully'})
                                else:
                                    Project.blockchain_count=0
                                    b=Project.blockchain_entry_count
                                    Project.blockchain_entry_count = b+1
                                    Project.save()
                                    ledger = blockchain_ledger()
                                    ledger.project_id=Project.id

                                    ledger.Remark=remark
                                    ledger.status='reject'
                                    ledger.blockchain_count=0
                                    ledger.blockchain_entry_count=b+1
                                    ledger.user_id=user.id
                                    ledger.save()

                                    encript = Blockchain_ledger_encripted()
                                    key = Fernet.generate_key()
                                    fernet = Fernet(key)

                                    blockchain_count_enc = "0"

                                    blockchain_entry_count_enc = "b+1"
                                    status_enc = 'reject'
                                    enc_remark = fernet.encrypt(remark.encode())
                                    enc_status_enc = fernet.encrypt(status_enc.encode())
                                    enc_blockchain_count_enc = fernet.encrypt(blockchain_count_enc.encode())
                                    enc_blockchain_entry_count_enc = fernet.encrypt(blockchain_entry_count_enc.encode())
                                    encript.project_id = Project.id
                                    username = user.first_name
                                    enc_username = fernet.encrypt(username.encode())
                                    encript.user_name = enc_username
                                    encript.Remark = enc_remark
                                    encript.status = enc_status_enc
                                    encript.blockchain_count = enc_blockchain_count_enc
                                    encript.blockchain_entry_count = enc_blockchain_entry_count_enc
                                    encript.user_id = user.id
                                    encript.save()
                                    return render(request,'employee/employee_index.html',{'message':'Reject Successfully'})


class view_block_chain(TemplateView):
    template_name = 'employee/view_block_chain.html'
    def get_context_data(self, **kwargs):
        context = super(view_block_chain,self).get_context_data(**kwargs)
        with open('json_data.json') as json_file:
             data = json.load(json_file)
        print(data)
        context['data'] = data
        return context

#
# class Remark(TemplateView):
#     template_name = 'employee/remarks.html'
#
#     def post(self, request, *args, **kwargs):
#         id = request.POST['id']
#         action = request.POST['action']
#         act = Compalaint.objects.get(id=id)
#         remarks=request.POST['remarks']
#         project=blockchain_ledger()
#         project.remarks=remarks
#         count1 = project.count
#         project.count = int(count1)+1
#         project.save()

class Apply_Leave(TemplateView):
    template_name = 'employee/apply_leave.html'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)

        types = request.POST['type']
        frodate = request.POST['fdate']
        noday = request.POST['nday']
        endd = request.POST['edate']
        period = request.POST['period']
        reason = request.POST['reason']
        employee = employee_details.objects.get(user_id=self.request.user.id)

        add = Leave()
        add.user=user
        add.employee = employee
        add.leavetype = types
        add.fromdate = frodate
        add.enddate = endd
        add.noday = noday
        add.leaveperiod = period
        add.reason = reason
        add.status = 'Apply'
        add.save()
        messages = "Successfully Applied"
        return render(request, 'employee/apply_leave.html', {'message': messages})



class Leave_status(TemplateView):
    template_name = 'employee/leave_status.html'

    def get_context_data(self, **kwargs):
        context = super(Leave_status, self).get_context_data(**kwargs)
        usid = self.request.user.id
        leave = Leave.objects.filter( user_id=usid)

        context['leave'] = leave
        return context


# class Notification(TemplateView):
#     template_name = 'employee/Project_notifications.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(Notification, self).get_context_data(**kwargs)
#         pro = blockchain_ledger.objects.all()
#
#         context['pro'] = pro
#         return context


class view_ledger_login(TemplateView):
    template_name = 'employee/view_ledger_login.html'
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        key = request.POST['key']
        project_id = self.request.GET['c_id']
        count =len(key)
        range = key[0:count:4]
        print(range)
        ascii_values=[]
        for i in range:
            print(i)
            ascii_values.append(ord(i))
        values_sum =sum(ascii_values)
        print(values_sum)
        print(1111111)

        if (Blockchain_admin.objects.filter(user_id=user,key2=values_sum,)):
            encript =blockchain_ledger.objects.filter(project_id=project_id)
            return render(request, 'employee/view_decripted_ledger.html', {'message': " login Successfully","encript":encript})

        else:

            encript =Blockchain_ledger_encripted.objects.filter(project_id=project_id)
            return render(request, 'employee/view_encripted_ledger.html', {'message': " invalid key","encript":encript})


class Profile_view(TemplateView):
    template_name = 'employee/profile.html'

    def get_context_data(self, **kwargs):
        cr = self.request.user.id
        context = super(Profile_view, self).get_context_data(**kwargs)
        employee = employee_details.objects.get(user_id=cr)
        block = Blockchain_admin.objects.get(user_id=cr)
        context['block'] = block

        context['employee'] = employee
        return context