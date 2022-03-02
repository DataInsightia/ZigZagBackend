from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q, Sum
from api import serializers
from api.models import *
from api.serializers import *
from random import randint
from api.utils import *
import json
import datetime

@api_view(['GET', 'POST'])
def test(request):
    return Response()

@api_view(['GET'])
def generate_orderid(request):
    try:
        start_order_number = 786

        if Order.objects.all().last() != None:
            order = Order.objects.all().last()
            last_order_id = order.order_id
            start_order_number = 786
            if int(last_order_id[2:])%1000 == 0:
                next_letter = chr(ord(last_order_id[1]) + 1)
                order_id = 'Z' + next_letter + str(start_order_number)
                return Response({'status': True, 'order_id': order_id})
            else:
                next_letter = chr(ord(last_order_id[1]) + 0)
                order_id = 'Z' + next_letter + str(int(last_order_id[2:]) + 1)
                return Response({'status': True, 'order_id': order_id})
        else:
            order_id = 'ZA' + str(start_order_number)
            return Response({'status': True, 'order_id' : order_id})
    except Exception as e:
        return Response({'status': True, 'error' : str(e)})

@api_view(['GET'])
def works(request):
    work = Work.objects.all()
    serializer = WorkSerializer(work, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializers(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def staff(request):
    staff = Staff.objects.all()
    serializer = StaffSerializers(staff, many=True)
    return Response(serializer.data)

@api_view(['GET','POST'])
def tmp_works(request):
    if request.method == 'POST':
        data = request.data
        if 'order_id' in data:
            order_id = data['order_id']
            try:
                if TmpWork.objects.filter(order_id=order_id).exists():
                    tmpwork = TmpWork.objects.filter(order_id=order_id)
                    total = tmpwork.aggregate(Sum('total'))
                    serializer = TmpWorkSerializer(tmpwork, many=True)
                    return Response({"data" : serializer.data, "total" : total})
                else:
                    return Response({'status': False,'message' : 'Order ID not found'})
            except Exception as e:
                return Response({'status': False, 'message': 'Failed', 'error': str(e)}, status.HTTP_400_BAD_REQUEST)
    return Response({'GET' : 'Not Allowed'})


@api_view(['GET','POST'])
def tmp_materials(request):
    if request.method == 'POST':
        data = request.data
        if 'order_id' in data:
            order_id = data['order_id']
            try:
                if TmpMaterial.objects.filter(order_id=order_id).exists():
                    tmp_material = TmpMaterial.objects.filter(order_id=order_id)
                    total = tmp_material.aggregate(Sum('total'))
                    serializer = TmpMaterialSerializer(tmp_material, many=True)
                    return Response({"data" : serializer.data, "total" : total})
                else:
                    return Response({'status': False,'message' : 'Order ID not found'})
            except Exception as e:
                return Response({'status': False, 'message': 'Failed', 'error': str(e)}, status.HTTP_400_BAD_REQUEST)
    return Response({'GET': 'Not Allowed'})

@api_view(['GET'])
def materials(request):
    material = Material.objects.all()
    serializer = MaterialSerializer(material, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def customer_details(request):
    if request.method == 'POST':
        data = request.data
        if 'cust_id' in data:
            cust_id = data['cust_id']
            try:
                if User.objects.filter(Q(mobile=cust_id) | Q(login_id=cust_id)).exists():
                    customer = Customer.objects.filter(mobile=cust_id)
                    serializer = CustomerSerializer(customer,many=True)
                    return Response(serializer.data)
                else:
                    return Response({'status': False, 'message': 'Failed', 'error': 'Customer Not Found!'},status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'status' : False,'message' : 'Failed','error' : str(e)},status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status' : False,'message' : 'Failed','error' : 'key missmatch'},status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def customer_login(request):
    if request.method == 'POST':
        data = request.data
        keys = ('cust_id','password')
        if all(i in data for i in keys):
            cust_id = data['cust_id']
            password = data['password']

            try:
                if User.objects.filter(Q(login_id=cust_id,password=password) | Q(mobile=cust_id,password=password)).exists():
                    auth = User.objects.filter(Q(login_id=cust_id,password=password) | Q(mobile=cust_id,password=password)).last()
                    user = UserSerializer(auth)
                    if auth.role == "staff":
                        staff = Staff.objects.get(staff_id = auth.login_id)
                        serializer = StaffSerializer(staff)
                        return Response({'status' : True, 'message': 'Success','data':serializer.data,'user':user.data})
                    elif auth.role == "customer":
                        customer = Customer.objects.get(cust_id = auth.login_id)
                        serializer = CustomerSerializer(customer)
                        return Response({'status' : True, 'message': 'Success','data':serializer.data,'user':user.data})
                    elif auth.role == "admin":
                        admin = User.objects.get(login_id = auth.login_id)
                        serializer = UserSerializer(admin)
                        return Response({'status' : True, 'message': 'Success','user':serializer.data})
                    else:
                        return Response({'status' : False, 'message': 'Failed'})
            except Exception as e:
                return Response({'status' : False,'message' : 'Failed','error' : str(e)})
        else:
            return Response({'status' : False,'message' : 'Failed','error' : 'key missmatch'})
    return Response({'GET' : 'Not Allowed'})


@api_view(['GET','POST'])
def customer_register(request):
    if request.method == 'POST':
        data = request.data
        keys = ('name', 'mobile','email','address','city','pincode','password')
        if all(i in data for i in keys):
            name = data['name']
            email = data['email']
            mobile = data['mobile']
            address = data['address']
            city = data['city']
            pincode = data['pincode']
            password = data['password']
            cust_id = "ZC" + str(randint(9999,100000))
            try:
                cust = Customer.objects.create(
                    cust_id = cust_id,
                    cust_name = name,
                    mobile = mobile,
                    email = email,
                    address=address,
                    password=password,
                    city = city,
                    pincode = pincode,
                )

                user = User.objects.create(
                    login_id = cust_id,
                    password = password,
                    mobile = mobile,
                    role= 'customer'
                )
                cust.save()
                user.save()
                return Response({'status' : True, 'message' : 'Success'})
            except Exception as e:
                return Response({'status' : False, 'error' : str(e)})
        return Response({'status' : False, 'message' : 'key error'})
    return Response({'GET': 'Not Allowed'})


@api_view(['GET','POST'])
def tmp_work(request):
    if request.method == 'POST':
        data = request.data
        keys = ('order_id','cust_id','work_id','qty','amount','total')
        if all(i in data for i in keys):
            order_id = data['order_id']
            work_id = data['work_id']
            cust_id = data['cust_id']
            qty = data['qty']
            amount = data['amount']
            total = data['total']

            try:
                work = Work.objects.get(work_id=work_id)
                tw = TmpWork.objects.create(
                    order_id = order_id,
                    work_id = work_id,
                    work_name = work.work_name,
                    cust_id = cust_id,
                    quantity = qty,
                    amount = amount,
                    total = total
                )
                tw.save()
                return Response({'status': True, 'message': 'Success'})
            except Exception as e:
                return Response({'status': False, 'error': str(e)})
        return Response({'status': False, 'message': 'key error'})
    return Response({'GET': 'Not Allowed'})

@api_view(['POST'])
def staff_register(request):
    if request.method == "POST":
        data = request.data
        print(data)
        staff_id = "ZS" + str(randint(9999,100000))
        keys = ('staff_name','password','mobile','address','city','salary_type','salary','worktype','acc_no','ifsc')
        if (i in data for i in keys):
            ifscdata = get_ifsc(data['ifsc']) 

            if User.objects.filter(mobile=data['mobile']).exists():
                return Response({'status' : False, 'message' : 'mobile number already exists'})
            else:
                try:
                    
                    staff = Staff.objects.create(
                        staff_id = staff_id,
                        staff_name = data['staff_name'],
                        mobile = data['mobile'],
                        address = data['address'],
                        city = data['city'],
                        salary_type = data['salary_type'],
                        salary = data['salary'],
                        acc_no = data['acc_no'],
                        bank = ifscdata['BANK'],
                        ifsc = ifscdata['IFSC'],
                        work_type = data['worktype'],
                        
                    )
                    user = User.objects.create(
                        login_id = staff_id,
                        password = data['password'],
                        mobile = data['mobile'],
                        role= 'staff'
                    )
                    staff.save()
                    user.save()

                    return Response({'status' : True, 'message' : 'Success'})
                except Exception as e:
                    return Response({'status' : False, 'error' : str(e)})
        else:
            return Response({'status' : False, 'message' : 'key error'})
    return Response({'GET': 'Not Allowed'})


@api_view(['GET','POST'])
def tmp_material(request):
    if request.method == 'POST':
        data = request.data
        keys = ('order_id','cust_id','material_id','qty','amount','total')
        if all(i in data for i in keys):
            order_id = data['order_id']
            material_id = data['material_id']
            cust_id = data['cust_id']
            qty = data['qty']
            amount = data['amount']
            total = data['total']

            try:
                material = Material.objects.get(material_id=material_id)
                tm = TmpMaterial.objects.create(
                    order_id = order_id,
                    material_id = material_id,
                    material_name = material.material_name,
                    cust_id = cust_id,
                    quantity = qty,
                    amount = amount,
                    total = total
                )
                tm.save()
                return Response({'status': True, 'message': 'Success'})
            except Exception as e:
                return Response({'status': False, 'error': str(e)})
        return Response({'status': False, 'message': 'key error'})
    return Response({'GET': 'Not Allowed'})

@api_view(['GET','POST'])
def del_tmpwork(request):
    if request.method == 'POST':
        data = request.data
        if 'id' in data:
            id = data['id']
            try:
                TmpWork.objects.get(id=id).delete()
            except Exception as e:
                return Response({'status': False, 'message': 'Failed', 'error': str(e)})
        else:
            return Response({'status': False, 'message': 'Failed', 'error': 'key missmatch'})
    return Response({'GET': 'Not Allowed'})

@api_view(['GET','POST'])
def del_tmpmaterial(request):
    if request.method == 'POST':
        data = request.data
        if 'id' in data:
            id = data['id']
            try:
                TmpMaterial.objects.get(id=id).delete()
            except Exception as e:
                return Response({'status': False, 'message': 'Failed', 'error': str(e)})
        else:
            return Response({'status': False, 'message': 'Failed', 'error': 'key missmatch'})
    return Response({'GET': 'Not Allowed'})


@api_view(['GET','POST'])
def get_tmpmaterial(request):
    if request.method == 'POST':
        data = request.data
        if all(i in data for i in ('order_id','material_id')):
            order_id = data['order_id']
            material_id = data['material_id']
            try:
                tmp_material = TmpMaterial.objects.get(order_id=order_id,material_id=material_id)
                serializer = TmpMaterialSerializer(tmp_material)
                return Response(serializer.data)
            except Exception as e:
                return Response({'status': False, 'message': 'Failed', 'error': str(e)})
        else:
            return Response({'status': False, 'message': 'Failed', 'error': 'key missmatch'})
    return Response({'GET': 'Not Allowed'})

@api_view(['GET','POST'])
def get_tmpwork(request):
    if request.method == 'POST':
        data = request.data
        if all(i in data for i in ('order_id','work_id')):
            order_id = data['order_id']
            work_id = data['work_id']
            try:
                tmp_work = TmpWork.objects.get(order_id=order_id,work_id=work_id)
                serializer = TmpWorkSerializer(tmp_work)
                return Response(serializer.data)
            except Exception as e:
                return Response({'status': False, 'message': 'Failed', 'error': str(e)})
        else:
            return Response({'status': False, 'message': 'Failed', 'error': 'key missmatch'})
    return Response({'GET': 'Not Allowed'})

@api_view(['GET','POST'])
def add_order_work(request):
    if request.method == 'POST':
        data = request.data
        keys = ('order_id','work_id','qty','work_amount')
        if all(i in data for i in keys):
            order_id = data['order_id']
            work_id = data['work_id']
            qty = data['qty']
            amount = data['work_amount']
            try:
                ow = OrderWork.objects.create(
                    order_id = order_id,
                    work_id = work_id,
                    quantity = qty,
                    amount = amount
                )
                ow.save()
                return Response({'status': True, 'message': 'Success'})
            except Exception as e:
                return Response({'status': False, 'message': 'Failed', 'error': str(e)})
        else:
            return Response({'status': False, 'message': 'Failed', 'error': 'key missmatch'})
    return Response({'GET': 'Not Allowed'})

@api_view(['GET','POST'])
def add_order_material(request):
    if request.method == 'POST':
        data = request.data
        keys = ('order_id','material_id','qty','material_amount')
        if all(i in data for i in keys):
            order_id = data['order_id']
            material_id = data['material_id']
            qty = data['qty']
            amount = data['material_amount']
            try:
                ow = OrderMaterial.objects.create(
                    order_id = order_id,
                    material_id = material_id,
                    quantity = qty,
                    amount = amount
                )
                ow.save()
                return Response({'status': True, 'message': 'Success'})
            except Exception as e:
                return Response({'status': False, 'message': 'Failed', 'error': str(e)})
        else:
            return Response({'status': False, 'message': 'Failed', 'error': 'key missmatch'})
    return Response({'GET': 'Not Allowed'})

@api_view(['GET','POST'])
def add_order(request):
    if request.method == 'POST':
        data = request.data
        keys = ('order_id','cust_id','due_date','pickup_type','total_amount','advance_amount','balance_amount')
        if all(i in data for i in keys):
            order_id = data['order_id']
            cust_id = data['cust_id']
            due_date = data['due_date']
            pickup_type = data['pickup_type']
            total_amount = data['total_amount']
            advance_amount = data['advance_amount']
            balance_amount = data['balance_amount']
            try:
                c_obj = Customer.objects.get(cust_id=cust_id)
                oo = Order.objects.create(
                    order_id = order_id,
                    customer = c_obj,
                    due_date=due_date,
                    pickup_type=pickup_type,
                    total_amount=total_amount,
                    advance_amount=advance_amount,
                    balance_amount=balance_amount
                )
                oo.save()
                return Response({'status': True, 'message': 'Success'})
            except Exception as e:
                return Response({'status': False, 'message': 'Failed', 'error': str(e)})
        else:
            return Response({'status': False, 'message': 'Failed', 'error': 'key missmatch'})
    return Response({'GET': 'Not Allowed'})
  
@api_view(['POST'])  
def staff_login(request):
    if request.method == 'POST':
        data = request.data
        keys = ('staff_id','password')
        if (i in data for i in keys):
            staff_id = data['staff_id']
            password = data['password']
            try:
                if User.objects.filter(Q(login_id=staff_id,password=password) | Q(mobile=staff_id,password=password)).exists():
                    try:
                        user = User.objects.get(mobile=staff_id,password=password)
                    except:
                        user = User.objects.get(login_id=staff_id,password=password)
                    return Response({'status' : True, 'message': 'Success','details':{"login_id":user.login_id,"mobile":user.mobile,"role":user.role}})
            except Exception as e:
                return Response({'status' : False,'message' : 'Failed','error' : str(e)})
        else:
            return Response({'status' : False,'message' : 'Failed','error' : 'key missmatch'})
    return Response({'GET' : 'Not Allowed'})

@api_view(['GET','POST'])
def order_status(request):
    if request.method == 'POST':
        data = request.data
        keys = ('cust_id','order_stage')
        if (i in data for i in keys):
            cust_id = data['cust_id']
            order_stage = data['order_stage']
            try:
                try:
                    customer = Customer.objects.get(cust_id = cust_id)
                except Customer.DoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                all_orders = []
                orders = Order.objects.filter(customer = customer)
                for order in orders:
                    if OrderWorkStaffStatusCompletion.objects.filter(order = order).exists():
                        add_order = OrderWorkStaffStatusCompletion.objects.filter(order = order,work_staff_completion_stage = order_stage)
                        serializer = OrderStatusSerializers(add_order,many=True)
                        all_orders.append(serializer.data)
                    else:
                        return Response([])
                return Response(all_orders)

            except Exception as e:
                return Response({'status' : False,'message' : 'Failed','error' : str(e)})
        else:
            return Response({'status' : False,'message' : 'Failed','error' : 'key missmatch'})
    return Response({'GET' : 'Not Allowed'})


@api_view(['GET','POST'])
def staff_work_assign(request):
    if request.method == "POST":
        data = request.data
        keys = ('staff_id','order_id','work_id','assign_stage','id')
        if (i in data for i in keys):
            staff_id = data['staff_id']
            order_id = data['order_id']
            work_id = data['work_id']
            assign_stage = data['assign_stage']
            id = data['id']
            try:
                
                order = fetchOrder(order_id)
                work = fetchWork(work_id)
                staff = fetchStaff(staff_id)

                if OrderWorkStaffAssign.objects.filter(order = order,work = work).exists():
                    OrderWorkStaffAssign.objects.filter(id = id,order = order,work = work).update(staff=staff,assign_stage = assign_stage,assign_date_time = datetime.datetime.now())
                    orderworkstaffassign = OrderWorkStaffAssign.objects.get(id = id,order = order,work = work)
                    try:
                        s = OrderWorkStaffStatusCompletion.objects.filter(order = order).last()
                        OrderWorkStaffStatusCompletion.objects.filter(id = s.id).update(order_next_stage_assign = True)
                    except:
                        pass
                    OrderWorkStaffTaken.objects.create(orderworkstaffassign = orderworkstaffassign,taken_stage = assign_stage)
                    resp = SuccessContext(True,'Success','Order assigned to staff')
                    return Response(resp) 
                else:
                    resp = SuccessContext(True,'Success','Order already assigned')
                    return Response(resp) 
            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False,'Failed','key missmatch')
            return Response(resp)

    elif request.method == 'GET':
        if True:
            li = []
            for i in OrderWorkStaffAssign.objects.filter(staff__isnull=True):
                order = OrderWorkStaffAssignSerializers(i)
                print(i)
                nextstage = getNextStage(i.order.order_id)
                data = {
                    "nextstage":nextstage,
                    "data":order.data
                }
                li.append(data)
            return Response({"data":li,"status":True,"message":"Success"},status.HTTP_200_OK) 
        else:
            resp = ErrorContext(False,'Failed','not found')
            return Response(resp)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def staff_work_assigned(request):
    if request.method == "POST":
        data = request.data
        keys = ('staff_id')
        if (i in data for i in keys):
            staff_id = data['staff_id']
            try:
                
                staff = fetchStaff(staff_id)
                if OrderWorkStaffTaken.objects.filter(taken_date_time__isnull = True).exists() and OrderWorkStaffAssign.objects.filter(staff = staff,assign_date_time__isnull = False).exists():
                    ordertaken = OrderWorkStaffTaken.objects.filter(taken_date_time__isnull = True)
                    serializer = OrderWorkStaffTakenSerializers(ordertaken,many=True)
                    return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 

                else:
                    return Response({"status":False,"message":"Failure"},status.HTTP_200_OK) 
            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False,'Failed','key missmatch')
            return Response(resp)

    elif request.method == 'GET':
        orders = OrderWorkStaffAssign.objects.all()
        serializer = OrderWorkStaffAssignSerializers(orders,many=True)
        return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def staff_work_taken(request):
    if request.method == "POST":     
        data = request.data
        keys = ('staff_id')
        if (i in data for i in keys):
            staff_id = data['staff_id']
            try:
                staff = fetchStaff(staff_id)

                if OrderWorkStaffTaken.objects.filter(orderworkstaffassign__staff_id = staff.staff_id).exists():
                   
                    ordertaken = OrderWorkStaffTaken.objects.exclude(orderworkstaffassign__staff_id = staff.staff_id,taken_date_time__isnull=True)
                    serializer = OrderWorkStaffTakenSerializers(ordertaken,many=True)
        
                    return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK)  
                else:
                    return Response({"status":False,"message":"Failed"},status.HTTP_200_OK) 
            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False,'Failed','key missmatch')
            return Response(resp)

    elif request.method == 'GET':
        
        orders = OrderWorkStaffAssign.objects.all()
        serializer = OrderWorkStaffAssignSerializers(orders,many=True)
        return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def staff_work_take(request):
    if request.method == "POST":
        data = request.data
       
        keys = ('staff_id','order_id','work_id','assigned_stage')
        if (i in data for i in keys):
            staff_id = data['staff_id']
            order_id = data['order_id']
            work_id = data['work_id']
            assigned_stage = data['assigned_stage']
            try:
                order = fetchOrder(order_id)
                work = fetchWork(work_id)
                staff = fetchStaff(staff_id)
                
                if  OrderWorkStaffAssign.objects.filter(order = order).exists():
                    ordw = OrderWorkStaffAssign.objects.filter(order = order).last()
                    OrderWorkStaffTaken.objects.filter(orderworkstaffassign = ordw).update(taken_date_time = datetime.datetime.now())
                    
                    if OrderWorkStaffStatusCompletion.objects.filter(order = order,staff = staff ,orderworkstaffassign = ordw).exists():
                        return Response({'status' : True, 'message': 'Success','details':'Order already taken'})  
                    else:
                        OrderWorkStaffStatusCompletion.objects.create(order = order,staff = staff ,orderworkstaffassign = ordw,work_staff_completion_stage = assigned_stage)
                        return Response({'status' : True, 'message': 'Success','details':'Order taken'})
                else:
                    return Response({'status' : True, 'message': 'Success','details':'order work already staff taken'})  
            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False,'Failed','key missmatch')
            return Response(resp)

    elif request.method == 'GET':
        
        orders = OrderWorkStaffAssign.objects.all()
        serializer = OrderWorkStaffAssignSerializers(orders,many=True)
        return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def staff_work_assign_completion(request):
    if request.method == "POST":
        data = request.data
        keys = ('staff')
        if (i in data for i in keys):
            try:
                staff_id = data['staff']
                staff = fetchStaff(staff_id)

                if OrderWorkStaffStatusCompletion.objects.exclude(work_completed_date_time__isnull=False).filter(staff=staff).exists():
                    ordc = OrderWorkStaffStatusCompletion.objects.exclude(work_completed_date_time__isnull=False).filter(staff=staff)
                    serializer = OrderWorkStaffAssignCompletionSerializers(ordc,many=True)
                    return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 
                else:
                    return Response({'status' : False, 'message': 'not found'})

            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            return Response({'status' : False,'message' : 'Failed','error' : 'key missmatch'}) 
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def staff_work_completion_review(request):
    if request.method == "POST":
        data = request.data
        keys = ('staff')
        if (i in data for i in keys):
            try:
                staff_id = data['staff']
                staff = fetchStaff(staff_id)

                if OrderWorkStaffStatusCompletion.objects.exclude(work_completed_date_time__isnull=True).exclude(work_staff_completion_approved = True).filter(staff=staff).exists():
                    ordc = OrderWorkStaffStatusCompletion.objects.exclude(work_completed_date_time__isnull=True).exclude(work_staff_completion_approved = True)
                    serializer = OrderWorkStaffAssignCompletionSerializers(ordc,many=True)
                    return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 
                else:
                    return Response({'status' : False, 'message': 'not found'})

            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            return Response({'status' : False,'message' : 'Failed','error' : 'key missmatch'}) 
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def staff_stage_completion(request):
    if request.method == "POST":
        data = request.data
        keys = ('staff_id','order_id','work_id','stage')
        if (i in data for i in keys):
            try:
                staff_id = data['staff_id']
                order_id = data['order_id']
                work_id = data['work_id']
                stage = data['stage']

                order = fetchOrder(order_id)
                staff = fetchStaff(staff_id)
                    
                if OrderWorkStaffStatusCompletion.objects.filter(staff = staff,order = order).exists():
                    ordc = OrderWorkStaffStatusCompletion.objects.filter(staff = staff,order = order).update(work_completed_date_time = datetime.datetime.now())
                    return Response({'status' : True, 'message': 'Success'})
                else:
                    return Response({'status' : False, 'message': 'not found'})

            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False,'Failed','key missmatch')
            return Response(resp)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def staff_work_assign_completion_app(request):
    if request.method == "POST":
        data = request.data
        keys = ('staff_id','order_id','work_id','stage','state')
        if (i in data for i in keys):
            try:
                staff_id = data['staff_id']
                order_id = data['order_id']
                work_id = data['work_id']
                stage = data['stage']
                state = data['state']

                order = fetchOrder(order_id)
                work = fetchWork(work_id)
                staff = fetchStaff(staff_id)

                if state == "approve":
                    if OrderWorkStaffStatusCompletion.objects.filter(staff = staff,order = order).exists():
                        ordc = OrderWorkStaffStatusCompletion.objects.filter(staff = staff,order = order).update(work_staff_comp_app_date_time = datetime.datetime.now(),work_staff_completion_approved = True)
                        OrderWorkStaffAssign.objects.create(order = order,work = work,staff=None)
                        resp = SuccessContext(True,'Success','Updated')
                        return Response(resp)
                    else:
                        resp = SuccessContext(True,'Success','Already Updated')
                        return Response(resp)
                elif state == "reassign":
                    OrderWorkStaffStatusCompletion.objects.filter(staff = staff,order = order).delete()
                    OrderWorkStaffTaken.objects.filter(staff = staff,order = order).delete()
                    OrderWorkStaffAssign.objects.filter(order = order,work = work).update(staff = None,assign_stage = None,assign_date_time = None)
                    resp = SuccessContext(True,'Success','deleted')
                    return Response(resp)

            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False,'Failed','key missmatch')
            return Response(resp)
    else:
        if OrderWorkStaffStatusCompletion.objects.filter(work_staff_completion_approved = False,work_completed_date_time__isnull=False).exists():
            ordc = OrderWorkStaffStatusCompletion.objects.filter(work_staff_completion_approved = False,work_completed_date_time__isnull=False)
            serializer = OrderWorkStaffAssignCompletionSerializers(ordc,many=True)
            return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 
        else:
            return Response({"status":False,"message":"Success"},status.HTTP_200_OK) 
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def work_finalize(request):
    if request.method == "POST":
        data = request.data
        keys = ('staff_id','order_id','work_id','stage','date')
        if (i in data for i in keys):
            try:
                staff_id = data['staff_id']
                order_id = data['order_id']
                work_id = data['work_id']
                stage = data['stage']
                date = data['date']

                order = fetchOrder(order_id)
                work = fetchWork(work_id)
                staff = fetchStaff(staff_id)

                if OrderWorkStaffStatusCompletion.objects.filter(staff = staff,order = order,work_staff_completion_approved = True).exists():
                    ordc = OrderWorkStaffStatusCompletion.objects.filter(staff = staff,order = order,work_staff_completion_approved = True).update(order_next_stage_assign = True)
                    OrderWorkStaffAssign.objects.create(order = order,work = work,staff=None)
                    resp = SuccessContext(True,'Success','Work finished')
                    return Response(resp)
                else:
                    resp = SuccessContext(True,'Failure','not allowed')
                    return Response(resp)

            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False,'Failed','key missmatch')
            return Response(resp)
    elif request.method == "GET":
        if OrderWorkStaffStatusCompletion.objects.filter(work_staff_completion_approved = True,order_next_stage_assign = False).exists():
            ordc = OrderWorkStaffStatusCompletion.objects.filter(work_staff_completion_approved = True,order_next_stage_assign = False)
            serializer = OrderWorkStaffAssignCompletionSerializers(ordc,many=True)
            return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 
        else:
            return Response({"status":False,"message":"Success"},status.HTTP_200_OK) 
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def staff_work_assign_completion_approval(request):
    if request.method == "POST":
        data = request.data
        keys = ('id','order_id','staff_id','work_id')
        if (i in data for i in keys):
            try:
                ids = int(data['id'])
                
                approval = True
                assignnextstage = True
                staff_id = data['staff_id']
                order_id = data['order_id']

                staff = fetchStaff(staff_id)
                order = fetchOrder(order_id)
                
                if OrderWorkStaffStatusCompletion.objects.filter(id = ids,work_staff_completion_approved = True).exists():
                    return Response({'status' : True, 'message': 'Success','details':'Order already approved'}) 
                else:
                    orderworkstaffstatuscompletion = OrderWorkStaffStatusCompletion.objects.get(id = ids)
                    orderworkstaffstatuscompletion.work_staff_completion_approved = approval
                    orderworkstaffstatuscompletion.order_next_stage_assign = assignnextstage
                    orderworkstaffstatuscompletion.save()

                    StaffWorkWage.objects.create(order = order, staff = staff,orderworkstatuscompletion = orderworkstaffstatuscompletion)

                    return Response({'status' : True, 'message': 'Success','details':'Order approved'}) 
            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False,'Failed','key missmatch')
            return Response(resp)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def staff_wage_calculation(request):
    if request.method == "POST":
        data = request.data
        keys = ('staff_id')
        if (i in data for i in keys):
            staff_id = data['staff_id']
            try:
 
                staff = fetchStaff(staff_id)
          

                if staff.salary_type == "monthly":
                    pass
                elif staff.salary_type == "wage":
                    if StaffWorkWage.objects.filter(staff = staff,wage_given = False).exists():
                        works = OrderWorkStaffStatusCompletion.objects.filter(staff = staff,work_staff_completion_approved = True)
                        for work in works:
                            if work.orderworkstaffassign.work.wage_type == "full":
                                amount = work.orderworkstaffassign.work.amount 
                                StaffWorkWage.objects.filter(staff = staff,wage_given = False,orderworkstatuscompletion = work).update(wage = amount)
                            elif work.orderworkstaffassign.work.wage_type == "half":
                                amount = work.orderworkstaffassign.work.amount/2
                                StaffWorkWage.objects.filter(staff = staff,wage_given = False,orderworkstatuscompletion = work).update(wage = amount)
                            elif work.orderworkstaffassign.work.wage_type == "10half":
                                amount = (work.orderworkstaffassign.work.amount-10)/2
                                StaffWorkWage.objects.filter(staff = staff,wage_given = False,orderworkstatuscompletion = work).update(wage = amount)
                            else:
                                pass
                    else:
                        pass       
                else:
                    return Response({'status' : False,'message' : 'Failed','error' : "please fill staff details"},status=status.HTTP_400_BAD_REQUEST)
                staffwages = StaffWorkWage.objects.filter(staff = staff)
                serializer = StaffWorkWageSerializers(staffwages,many=True)
                return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 
            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False,'Failed','key missmatch')
            return Response(resp)

    elif request.method == 'GET':
        staffwages = StaffWorkWage.objects.all()
        serializer = StaffWorkWageSerializers(staffwages,many=True)
        return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def staff_wage_manager(request):
    if request.method == "POST":
        data = request.data
        keys = ('staff_id')
        if (i in data for i in keys):
            staff_id = data['staff_id']
            try:
               
                staff = fetchStaff(staff_id)

                staffwages = StaffWorkWage.objects.filter(staff = staff)
                serializer = StaffWorkWageSerializers(staffwages,many=True)
                return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 
            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False,'Failed','key missmatch')
            return Response(resp)

    elif request.method == 'GET':
        staffwages = StaffWorkWage.objects.all()
        serializer = StaffWorkWageSerializers(staffwages,many=True)
        return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 
    return Response(serializers.data,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def staff_payment_update(request):
    if request.method == "POST":
        data = request.data
        keys = ('staff_id','updated_amount')
        if (i in data for i in keys):
            staff_id = data['staff_id']
            updated_amount = data['updated_amount']
            try:
                
                staff = fetchStaff(staff_id)
                 
            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False,'Failed','key missmatch')
            return Response(resp)

    elif request.method == 'GET':
        staffwages = StaffWorkWage.objects.all()
        serializer = StaffWorkWageSerializers(staffwages,many=True)
        return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 

@api_view(['GET','POST'])
def manager_dashboard(request):
    if request.method == "POST":
        data = request.data
        keys = ('staff_id')
        if (i in data for i in keys):
            staff_id = data['staff_id']
            try:
                
                staff = fetchStaff(staff_id)
                # staffwages = StaffWorkWage.objects.filter(staff = staff)
                # serializers = StaffWorkWageSerializers(staffwages,many=True)
                # return Response(serializers.data) 
            except Exception as e:
                resp = KeyErrorContext(False,'Failed',str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False,'Failed','key missmatch')
            return Response(resp)

    elif request.method == 'GET':
        staffwages = StaffWorkWage.objects.all()
        serializer = StaffWorkWageSerializers(staffwages,many=True)
        return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK) 

class OrderWorkStaffAssignView(APIView):
    def get(self,request):
        model = OrderWorkStaffAssign.objects.all()
        serializer = OrderWorkStaffAssignSerializer(model,many=True)
        return Response(serializer.data)

    def get(self,order_id):
        model = OrderWorkStaffAssign.objects.filter(order_id=order_id)
        serializer = OrderWorkStaffAssignSerializer(model,many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        keys = ("order_id","work_id","order_work_label")
        if all(i in data for i in keys):
            
            try:
                order = Order.objects.get(order_id=data['order_id'])
                work = Work.objects.get(work_id=data['work_id'])
                order_work_label = data['order_work_label']
                OrderWorkStaffAssign.objects.create(
                    order = order,
                    work = work,
                    order_work_label = order_work_label,
                    staff = None
                ).save()
                return Response({"status": True,"message" : "Inserted"},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status": False,"message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        data = request.data
        if 'order_id' in data:
            order = Order.objects.get(order_id=data['order_id'])
            try:
                OrderWorkStaffAssign.objects.get(order=order).delete()
            except Exception as e:
                return Response({"status": False,"message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        data = request.data
        keys = ("order_id","work_id","staff_id","assign_stage","assign_date_time")
        if all(i in data for i in keys):
            order = Order.objects.get(order_id=data['order_id'])
            work = Work.objects.get(work_id=data['work_id'])
            staff = Staff.objects.get(staff_id = data['staff_id'])
            try:
                OrderWorkStaffAssign.objects.get(order=order,assign_stage="").update(
                    order = order,
                    work = work,
                    staff = staff,
                    assign_stage = data['assign_stage'],
                    assign_date_time = data['assign_date_time']
                )
                return Response({"status": True,"message" : "Updated"},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status": False,"message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


class StaffWorkWageView(APIView):
    def post(self,request):
        data = request.data
        keys = ("order_id","staff_id","work_id")
        if all(i in data for i in keys):
            staff = Staff.objects.get(staff_id = data['staff_id'])
            order = Order.objects.get(order_id = data['order_id'])
            work = Work.objects.get(work=data['work'])
            try:
                StaffWorkWage.objects.create(
                    staff=staff,
                    order=order,
                    work=work,
                    work_staff_approval_date_time = None,
                    completion_date_time = None,
                    wage=None,
                    wage_given=None
                    ).save()
                return Response({"status": True,"message" : "Inserted"},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status": False,"message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        data = request.data
        if 'id' in data:
            id = data['id']
            try:
                StaffWorkWage.objects.get(id=id).delete()
                return Response({"status": True,"message" : "Deleted"},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status": False,"message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


class StaffWageGivenStatusView(APIView):
    def post(self,request):
        data = request.data
        keys = ("order_id","staff_id","work_id")
        if all(i in data for i in keys):
            staff = Staff.objects.get(staff_id = data['staff_id'])
            order = Order.objects.get(order_id = data['order_id'])
            work = Work.objects.get(work=data['work'])
            try:
                StaffWageGivenStatus.objects.create(
                    staff=staff,
                    order=order,
                    work=work,
                    wage_from_date = None,
                    wage_to_date = None,
                    wage_given_date = None,
                    total_wage_given = None,
                    wage_payment_reference_no = None,
                    wage_payment_reference_image = None
                    ).save()
                return Response({"status": True,"message" : "Inserted"},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status": False,"message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        data = request.data
        if 'id' in data:
            id = data['id']
            try:
                StaffWageGivenStatus.objects.get(id=id).delete()
                return Response({"status": True,"message" : "Deleted"},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status": False,"message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


def upload_file(request):

    name = request['name']
    file = request.FILES['file']

    try:
        UploadFile.objects.create(name=name,file=file)
        return Response({"status": True,"message" : "Deleted"},status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"status": False,"message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
