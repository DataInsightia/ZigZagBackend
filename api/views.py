from ast import Del
from dis import dis
from math import prod
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q, Sum, Count
from api import serializers
from api.models import *
from api.serializers import *
from random import randint
from api.utils import *
import json
import datetime
from dateutil.relativedelta import *


@api_view(["GET", "POST"])
def test(request):
    return Response()


@api_view(["GET"])
def generate_orderid(request):
    try:
        start_order_number = 786

        if Order.objects.all().last() != None:
            order = Order.objects.all().last()
            last_order_id = order.order_id
            start_order_number = 786
            if int(last_order_id[2:]) % 1000 == 0:
                next_letter = chr(ord(last_order_id[1]) + 1)
                order_id = "Z" + next_letter + str(start_order_number)
                return Response({"status": True, "order_id": order_id})
            else:
                next_letter = chr(ord(last_order_id[1]) + 0)
                order_id = "Z" + next_letter + str(int(last_order_id[2:]) + 1)
                return Response({"status": True, "order_id": order_id})
        else:
            order_id = "ZA" + str(start_order_number)
            return Response({"status": True, "order_id": order_id})
    except Exception as e:
        return Response({"status": True, "error": str(e)})


class works(APIView):
    def get(self, request):
        work = Work.objects.all()
        serializer = WorkSerializer(work, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response([], status=status.HTTP_201_CREATED)


    def post(self, request):
        data = request.data
        if data["work_name"] and data["amount"] and data["wage_type"]:
            work_id = generate_ID("ZW", Work)
            Work.objects.create(
                work_name=data["work_name"],
                amount=data["amount"],
                wage_type=data["wage_type"],
                work_id=work_id,
            )
            resp = SuccessContext(True, "Success", "Work added")
            return Response(resp, status=status.HTTP_201_CREATED)
        resp = ErrorContext(False, "Failure", "Please enter valid data")
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        if request.method == "PUT":
            work = Work.objects.get(work_id=data["work_id"])
            work.work_name = data["work_name"]
            work.amount = data["amount"]
            work.wage_type = data["wage_type"]
            work.save()
            resp = SuccessContext(True, "Success", "Work updated")
            return Response(resp, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, work_id):
        try:
            work_id = Work.objects.get(work_id=work_id)
        except:
            resp = ErrorContext(False, "Failure", "work id not found")
            return Response(resp, status=status.HTTP_404_NOT_FOUND)
        if work_id:
            Work.objects.filter(work_id=work_id.work_id).delete()
            resp = SuccessContext(True, "Success", "Work deleted")
            return Response(resp, status=status.HTTP_201_CREATED)
        resp = ErrorContext(False, "Failure", "Please enter valid data")
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def workdetail(request,work_id):
    work = Work.objects.get(work_id = work_id)
    serializer = WorkSerializer(work)
    return Response(serializer.data)

@api_view(["GET"])
def materialdetail(request,material_id):
    material = Material.objects.get(material_id = material_id)
    serializer = MaterialSerializer(material)
    return Response(serializer.data)
 

class MaterialView(APIView):
    def get(self, request):
        material = Material.objects.all()
        serializer = MaterialSerializer(material, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response([], status=status.HTTP_201_CREATED)

    def post(self, request):
        data = request.data
        print(data)
        if data["material_name"] and data["measurement"] and data["amount"]:
            material_id = generate_ID("ZM", Material)
            Material.objects.create(
                material_id=material_id,
                amount=data["amount"],
                material_name=data["material_name"],
                measurement=data["measurement"],
            )
            resp = SuccessContext(True, "Success", "Material added")
            return Response(resp, status=status.HTTP_201_CREATED)
        resp = ErrorContext(False, "Failure", "Please enter valid data")
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        if request.method == "PUT":
            material = Material.objects.get(material_id=data["material_id"])
            material.material_name = data["material_name"]
            material.amount = data["amount"]
            material.measurement = data["measurement"]
            material.save()
            resp = SuccessContext(True, "Success", "Material updated")
            return Response(resp, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, mat_id):
        try:
            material_id = Material.objects.get(material_id=mat_id)
        except:
            resp = ErrorContext(False, "Failure", "Material id not found")
            return Response(resp, status=status.HTTP_404_NOT_FOUND)
        if mat_id:
            Material.objects.filter(material_id=material_id.material_id).delete()
            resp = SuccessContext(True, "Success", "Material deleted")
            return Response(resp, status=status.HTTP_201_CREATED)
        resp = ErrorContext(False, "Failure", "Please enter valid data")
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializers(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def staff(request):
    staff = Staff.objects.all()
    serializer = StaffSerializers(staff, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def tmp_works(request):
    if request.method == "POST":
        data = request.data
        if "order_id" in data:
            order_id = data["order_id"]
            try:
                if TmpWork.objects.filter(order_id=order_id).exists():
                    tmpwork = TmpWork.objects.filter(order_id=order_id)
                    total = tmpwork.aggregate(Sum("total"))
                    serializer = TmpWorkSerializer(tmpwork, many=True)
                    return Response({"data": serializer.data, "total": total})
                else:
                    return Response({"status": False, "message": "Order ID not found"})
            except Exception as e:
                return Response(
                    {"status": False, "message": "Failed", "error": str(e)},
                    status.HTTP_400_BAD_REQUEST,
                )
    return Response({"GET": "Not Allowed"})


@api_view(["GET", "POST"])
def tmp_materials(request):
    if request.method == "POST":
        data = request.data
        if "order_id" in data:
            order_id = data["order_id"]
            try:
                if TmpMaterial.objects.filter(order_id=order_id).exists():
                    tmp_material = TmpMaterial.objects.filter(order_id=order_id)
                    total = tmp_material.aggregate(Sum("total"))
                    serializer = TmpMaterialSerializer(tmp_material, many=True)
                    return Response({"data": serializer.data, "total": total})
                else:
                    return Response({"status": False, "message": "Order ID not found"})
            except Exception as e:
                return Response(
                    {"status": False, "message": "Failed", "error": str(e)},
                    status.HTTP_400_BAD_REQUEST,
                )
    return Response({"GET": "Not Allowed"})


@api_view(["GET"])
def materials(request):
    material = Material.objects.all()
    serializer = MaterialSerializer(material, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def customer_details(request):
    if request.method == "POST":
        data = request.data
        if "cust_id" in data:
            cust_id = data["cust_id"]
            try:
                if User.objects.filter(
                    Q(mobile=cust_id) | Q(login_id=cust_id)
                ).exists():
                    customer = Customer.objects.filter(
                        Q(mobile=cust_id) | Q(cust_id=cust_id)
                    )
                    serializer = CustomerSerializer(customer, many=True)
                    return Response(serializer.data)
                else:
                    return Response(
                        {
                            "status": False,
                            "message": "Failed",
                            "error": "Customer Not Found!",
                        },
                        status.HTTP_400_BAD_REQUEST,
                    )
            except Exception as e:
                return Response(
                    {"status": False, "message": "Failed", "error": str(e)},
                    status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"status": False, "message": "Failed", "error": "key missmatch"},
                status.HTTP_400_BAD_REQUEST,
            )


@api_view(["POST"])
def customer_login(request):
    if request.method == "POST":
        data = request.data
        keys = ("cust_id", "password")
        if all(i in data for i in keys):
            cust_id = data["cust_id"]
            password = data["password"]

            try:
                if User.objects.filter(
                    Q(login_id=cust_id, password=password)
                    | Q(mobile=cust_id, password=password)
                ).exists():
                    auth = User.objects.filter(
                        Q(login_id=cust_id, password=password)
                        | Q(mobile=cust_id, password=password)
                    ).last()
                    user = UserSerializer(auth)
                    if auth.role == "staff":
                        staff = Staff.objects.get(staff_id=auth.login_id)
                        serializer = StaffSerializer(staff)
                        return Response(
                            {
                                "status": True,
                                "message": "Success",
                                "data": serializer.data,
                                "user": user.data,
                            }
                        )
                    elif auth.role == "customer":
                        customer = Customer.objects.get(cust_id=auth.login_id)
                        serializer = CustomerSerializer(customer)
                        return Response(
                            {
                                "status": True,
                                "message": "Success",
                                "data": serializer.data,
                                "user": user.data,
                            }
                        )
                    elif auth.role == "admin":
                        admin = User.objects.get(login_id=auth.login_id)
                        serializer = UserSerializer(admin)
                        return Response(
                            {
                                "status": True,
                                "message": "Success",
                                "user": serializer.data,
                            }
                        )
                    else:
                        return Response({"status": False, "message": "Failed"})
            except Exception as e:
                return Response({"status": False, "message": "Failed", "error": str(e)})
        else:
            return Response(
                {"status": False, "message": "Failed", "error": "key missmatch"}
            )
    return Response({"GET": "Not Allowed"})


@api_view(["PUT", "POST"])
def customer_register(request):
    if request.method == "POST":
        data = request.data
        keys = ("name", "mobile", "email", "address", "city", "pincode", "password")
        if all(i in data for i in keys):
            name = data["name"]
            email = data["email"]
            mobile = data["mobile"]
            address = data["address"]
            city = data["city"]
            pincode = data["pincode"]
            password = data["password"]
            cust_id = "ZC" + str(randint(9999, 100000))
            try:
                cust = Customer.objects.create(
                    cust_id=cust_id,
                    cust_name=name,
                    mobile=mobile,
                    email=email,
                    address=address,
                    password=password,
                    city=city,
                    pincode=pincode,
                )

                user = User.objects.create(
                    login_id=cust_id, password=password, mobile=mobile, role="customer"
                )
                cust.save()
                user.save()
                return Response({"status": True, "message": "Success"})
            except Exception as e:
                return Response({"status": False, "error": str(e)})
        return Response({"status": False, "message": "key error"})
    if request.method == "PUT":
        cust_id = request.data.get("cust_id")
        try:
            customer = Customer.objects.get(cust_id=cust_id)
            customer.cust_name = request.data.get("username")
            customer.address = request.data.get("address")
            customer.city = request.data.get("city")
            customer.pincode = request.data.get("pincode")

            customer.save()
            return Response({"status": True, "message": "Success"})
        except:
            return Response({"status": False, "message": "Failure"})
    return Response({"GET": "Not Allowed"})


@api_view(["GET", "POST"])
def tmp_work(request):
    if request.method == "POST":
        data = request.data
        keys = ("order_id", "cust_id", "work_id", "qty", "amount", "total")
        if all(i in data for i in keys):
            order_id = data["order_id"]
            work_id = data["work_id"]
            cust_id = data["cust_id"]
            qty = data["qty"]
            amount = data["amount"]
            total = data["total"]

            try:
                work = Work.objects.get(work_id=work_id)
                tw = TmpWork.objects.create(
                    order_id=order_id,
                    work_id=work_id,
                    work_name=work.work_name,
                    cust_id=cust_id,
                    quantity=qty,
                    amount=amount,
                    total=total,
                )
                tw.save()
                return Response(
                    {"status": True, "message": "Success"},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response({"status": False, "error": str(e)})
        return Response({"status": False, "message": "key error"})
    return Response({"GET": "Not Allowed"})


@api_view(["POST", "PUT"])
def staff_register(request):
    if request.method == "POST":
        data = json.loads(request.POST["data"])
        staff_id = "ZS" + str(randint(9999, 100000))
        keys = (
            "staff_name",
            "password",
            "mobile",
            "address",
            "city",
            "salary_type",
            "salary",
            "worktype",
            "acc_no",
            "ifsc",
        )
        if (i in data for i in keys):
            ifscdata = get_ifsc(data["ifsc"])

            if User.objects.filter(mobile=data["mobile"]).exists():
                return Response(
                    {"status": False, "message": "mobile number already exists"}
                )
            else:
                try:

                    staff = Staff.objects.create(
                        staff_id=staff_id,
                        staff_name=data["staff_name"],
                        mobile=data["mobile"],
                        address=data["address"],
                        city=data["city"],
                        salary_type=data["salary_type"],
                        salary=data["salary"],
                        acc_no=data["acc_no"],
                        bank="", #ifscdata["BANK"],
                        ifsc=ifscdata["IFSC"],
                        work_type=data["worktype"],
                        photo=request.FILES.get("file"),
                    )
                    user = User.objects.create(
                        login_id=staff_id,
                        password=data["password"],
                        mobile=data["mobile"],
                        role="staff",
                    )
                    staff.save()
                    user.save()

                    return Response({"status": True, "message": "Success"})
                except Exception as e:
                    return Response({"status": False, "error": str(e)})
        else:
            return Response({"status": False, "message": "key error"})

    if request.method == "PUT":
        staff_id = request.data.get("staff_id")
        try:
            staff = Staff.objects.get(staff_id = staff_id)
            # staff.photo = request.FILES.get('file')
            staff.staff_name = request.data.get('username')
            staff.address = request.data.get('address')
            staff.city = request.data.get('city')
            staff.ifsc = request.data.get('ifsc')
            staff.bank = request.data.get('bank')
            staff.work_type = request.data.get('work_type')
            staff.acc_no = request.data.get('acc_no')
            staff.save()
            Staff.objects.filter(staff_id = staff_id).update(photo = request.FILES.get('file'))
            return Response({'status' : True, 'message' : 'Success'})
        except:
            return Response({"status": False, "message": "Failure"})
    return Response({"GET": "Not Allowed"})


@api_view(["GET", "POST"])
def tmp_material(request):
    if request.method == "POST":
        data = request.data
        keys = ("order_id", "cust_id", "material_id", "qty", "amount", "total")
        if all(i in data for i in keys):
            order_id = data["order_id"]
            material_id = data["material_id"]
            cust_id = data["cust_id"]
            qty = data["qty"]
            amount = data["amount"]
            total = data["total"]

            try:
                material = Material.objects.get(material_id=material_id)
                tm = TmpMaterial.objects.create(
                    order_id=order_id,
                    material_id=material_id,
                    material_name=material.material_name,
                    cust_id=cust_id,
                    quantity=qty,
                    amount=amount,
                    total=total,
                )
                tm.save()
                return Response({"status": True, "message": "Success"})
            except Exception as e:
                return Response({"status": False, "error": str(e)})
        return Response({"status": False, "message": "key error"})
    return Response({"GET": "Not Allowed"})


@api_view(["GET", "POST"])
def del_tmpwork(request):
    if request.method == "POST":
        data = request.data
        if "id" in data:
            id = data["id"]
            try:
                TmpWork.objects.get(id=id).delete()
            except Exception as e:
                return Response({"status": False, "message": "Failed", "error": str(e)})
        else:
            return Response(
                {"status": False, "message": "Failed", "error": "key missmatch"}
            )
    return Response({"GET": "Not Allowed"})


@api_view(["GET", "POST"])
def del_tmpmaterial(request):
    if request.method == "POST":
        data = request.data
        if "id" in data:
            id = data["id"]
            try:
                TmpMaterial.objects.get(id=id).delete()
            except Exception as e:
                return Response({"status": False, "message": "Failed", "error": str(e)})
        else:
            return Response(
                {"status": False, "message": "Failed", "error": "key missmatch"}
            )
    return Response({"GET": "Not Allowed"})


@api_view(["GET", "POST"])
def get_tmpmaterial(request):
    if request.method == "POST":
        data = request.data
        if all(i in data for i in ("order_id", "material_id")):
            order_id = data["order_id"]
            material_id = data["material_id"]
            try:
                tmp_material = TmpMaterial.objects.get(
                    order_id=order_id, material_id=material_id
                )
                serializer = TmpMaterialSerializer(tmp_material)
                return Response(serializer.data)
            except Exception as e:
                return Response({"status": False, "message": "Failed", "error": str(e)})
        else:
            return Response(
                {"status": False, "message": "Failed", "error": "key missmatch"}
            )
    return Response({"GET": "Not Allowed"})


@api_view(["GET", "POST"])
def get_tmpwork(request):
    if request.method == "POST":
        data = request.data
        if all(i in data for i in ("order_id", "work_id")):
            order_id = data["order_id"]
            work_id = data["work_id"]
            try:
                tmp_work = TmpWork.objects.get(order_id=order_id, work_id=work_id)
                serializer = TmpWorkSerializer(tmp_work)
                return Response(serializer.data)
            except Exception as e:
                return Response({"status": False, "message": "Failed", "error": str(e)})
        else:
            return Response(
                {"status": False, "message": "Failed", "error": "key missmatch"}
            )
    return Response({"GET": "Not Allowed"})


@api_view(["GET", "POST"])
def add_order_work(request):
    if request.method == "POST":
        data = request.data
        keys = ("order_id", "work_id", "qty", "work_amount", "work_name")
        if all(i in data for i in keys):
            order_id = data["order_id"]
            work_id = data["work_id"]
            qty = data["qty"]
            amount = data["work_amount"]
            work_name = data["work_name"]
            try:
                ow = OrderWork.objects.create(
                    order_id=order_id,
                    work_id=work_id,
                    quantity=qty,
                    amount=amount,
                    work_name=work_name,
                )
                ow.save()
                return Response({"status": True, "message": "Success"})
            except Exception as e:
                return Response({"status": False, "message": "Failed", "error": str(e)})
        else:
            return Response(
                {"status": False, "message": "Failed", "error": "key missmatch"}
            )
    return Response({"GET": "Not Allowed"})


@api_view(["GET", "POST"])
def add_order_material(request):
    if request.method == "POST":
        data = request.data
        keys = ("order_id", "material_id", "qty", "material_amount", "material_name")
        if all(i in data for i in keys):
            order_id = data["order_id"]
            material_id = data["material_id"]
            qty = data["qty"]
            amount = data["material_amount"]
            material_name = data["material_name"]
            try:
                ow = OrderMaterial.objects.create(
                    order_id=order_id,
                    material_id=material_id,
                    quantity=qty,
                    amount=amount,
                    material_name=material_name,
                )
                ow.save()
                return Response({"status": True, "message": "Success"})
            except Exception as e:
                return Response({"status": False, "message": "Failed", "error": str(e)})
        else:
            return Response(
                {"status": False, "message": "Failed", "error": "key missmatch"}
            )
    return Response({"GET": "Not Allowed"})


@api_view(["GET", "POST"])
def add_order(request):
    if request.method == "POST":
        data = request.data
        keys = (
            "order_id",
            "cust_id",
            "due_date",
            "pickup_type",
            "total_amount",
            "advance_amount",
            "balance_amount",
            "courier_amount",
            "courier_address",
        )
        if all(i in data for i in keys):
            order_id = data["order_id"]
            cust_id = data["cust_id"]
            due_date = data["due_date"]
            pickup_type = data["pickup_type"]
            total_amount = data["total_amount"]
            advance_amount = data["advance_amount"]
            balance_amount = data["balance_amount"]
            courier_amount = data["courier_amount"]
            courier_address = data["courier_address"]

            try:
                c_obj = Customer.objects.get(cust_id=cust_id)
                oo = Order.objects.create(
                    order_id=order_id,
                    customer=c_obj,
                    due_date=due_date,
                    pickup_type=pickup_type,
                    total_amount=total_amount,
                    advance_amount=advance_amount,
                    balance_amount=balance_amount,
                    courier_amount=courier_amount,
                    courier_address=courier_address,
                )
                oo.save()
                return Response({"status": True, "message": "Success"})
            except Exception as e:
                return Response({"status": False, "message": "Failed", "error": str(e)})
        else:
            return Response(
                {"status": False, "message": "Failed", "error": "key missmatch"}
            )
    return Response({"GET": "Not Allowed"})


# @api_view(['POST'])
# def staff_login(request):
#     if request.method == 'POST':
#         data = request.data
#         keys = ('staff_id','password')
#         if (i in data for i in keys):
#             staff_id = data['staff_id']
#             password = data['password']
#             try:
#                 if User.objects.filter(Q(login_id=staff_id,password=password) | Q(mobile=staff_id,password=password)).exists():
#                     try:
#                         user = User.objects.get(mobile=staff_id,password=password)
#                     except:
#                         user = User.objects.get(login_id=staff_id,password=password)
#                     return Response({'status' : True, 'message': 'Success','details':{"login_id":user.login_id,"mobile":user.mobile,"role":user.role}})
#             except Exception as e:
#                 return Response({'status' : False,'message' : 'Failed','error' : str(e)})
#         else:
#             return Response({'status' : False,'message' : 'Failed','error' : 'key missmatch'})
#     return Response({'GET' : 'Not Allowed'})


@api_view(["GET", "POST"])
def order_status(request):
    if request.method == "POST":
        data = request.data
        keys = "order_id"
        if (i in data for i in keys):
            # cust_id = data['cust_id']
            order_id = data["order_id"]
            order = fetchOrder(order_id)
            try:
                ords = OrderWorkStaffStatusCompletion.objects.filter(
                    order=order,
                    work_staff_completion_approved=True,
                ).order_by("-work_staff_comp_app_date_time")

                include_res = []
                for i in ords:
                    exclude_list = [
                        "cutting",
                        "stitching",
                        "hook",
                        "overlock",
                        "Completed",
                    ]

                    if i.work_staff_completion_stage in exclude_list:
                        exclude_list.remove(i.work_staff_completion_stage)
                        include_res.append(
                            {"stage": i.work_staff_completion_stage, "status": True}
                        )
                    else:
                        pass
                    try:
                        for e in exclude_list:
                            include_res.append({"stage": e, "status": False})
                    except:
                        pass

                resp = SuccessContext(True, "Success", include_res)
                return Response(resp)
            except Exception as e:
                return Response({"status": False, "message": "Failed", "error": str(e)})
        else:
            return Response(
                {"status": False, "message": "Failed", "error": "key missmatch"}
            )
    return Response({"GET": "Not Allowed"})

@api_view(["GET","POST"])
def staff_work_assign_by_order(request):
    if request.method == 'POST':
        order_id = request.data['order_id']
        li = []
        for i in OrderWorkStaffAssign.objects.filter(order__order_id = order_id,staff__isnull=True):
            order = OrderWorkStaffAssignSerializers(i)
            nextstage = getNextStage(i.order.order_id, i.order_work_label)
            data = {"nextstage": nextstage, "data": order.data}
            li.append(data)
        return Response(
            {"data": li, "status": True, "message": "Success"}, status.HTTP_200_OK
        )
    
@api_view(["GET", "POST"])
def staff_work_assign(request):
    if request.method == "POST":
        data = request.data
        keys = ("staff_id", "order_id", "work_id", "assign_stage", "id","material_location")
        if all(i in data for i in keys):
            staff_id = data["staff_id"]
            order_id = data["order_id"]
            work_id = data["work_id"]
            assign_stage = data["assign_stage"]
            id = data["id"]
            material_location = data["material_location"]
            order_work_label = data["order_work_label"]
            try:
                order = fetchOrder(order_id)
                work = fetchWork(work_id)
                staff = fetchStaff(staff_id)

                if OrderWorkStaffAssign.objects.filter(
                    order=order, work=work, order_work_label=order_work_label
                ).exists():
                    OrderWorkStaffAssign.objects.filter(
                        id=id, order=order, work=work, order_work_label=order_work_label
                    ).update(
                        staff=staff,
                        assign_stage=assign_stage,
                        assign_date_time=datetime.datetime.now(),
                        material_location=material_location,
                    )
                    orderworkstaffassign = OrderWorkStaffAssign.objects.get(
                        id=id, order=order, work=work, order_work_label=order_work_label
                    )
                    try:
                        s = OrderWorkStaffStatusCompletion.objects.filter(
                            order=order
                        ).last()
                        OrderWorkStaffStatusCompletion.objects.filter(id=s.id).update(
                            order_next_stage_assign=True
                        )
                    except:
                        pass
                    if assign_stage == "Completed":
                        orderworkstaffassign.assign_stage = "complete_final_stage"
                        orderworkstaffassign.save()

                        StaffWorkWage.objects.create(
                            staff=staff,
                            work=work,
                            order=order,
                            work_staff_approval_date_time=s.work_staff_comp_app_date_time,
                        )
                        return Response(resp)
                    else:
                        OrderWorkStaffTaken.objects.create(
                            orderworkstaffassign=orderworkstaffassign,
                            taken_stage=assign_stage,
                        )
                        resp = SuccessContext(
                            True, "Success", "Order assigned to staff"
                        )
                        return Response(resp)
                else:
                    resp = SuccessContext(True, "Success", "Order already assigned")
                    return Response(resp)
            except Exception as e:
                resp = KeyErrorContext(False, "Failed", str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False, "Failed", "key missmatch")
            return Response(resp)

    elif request.method == "GET":
        if True:
            li = []
            for i in OrderWorkStaffAssign.objects.filter(work__isnull = False,staff__isnull=True):
                order = OrderWorkStaffAssignSerializers(i)
                nextstage = getNextStage(i.order.order_id, i.order_work_label)
                data = {"nextstage": nextstage, "data": order.data}
                li.append(data)
            return Response(
                {"data": li, "status": True, "message": "Success"}, status.HTTP_200_OK
            )
        else:
            resp = ErrorContext(False, "Failed", "not found")
            return Response(resp)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def staff_work_assigned(request):
    if request.method == "POST":
        data = request.data
        keys = "staff_id"
        if (i in data for i in keys):
            staff_id = data["staff_id"]
            try:

                staff = fetchStaff(staff_id)
                if (
                    OrderWorkStaffTaken.objects.filter(
                        taken_date_time__isnull=True
                    ).exists()
                    and OrderWorkStaffAssign.objects.filter(
                        staff=staff, assign_date_time__isnull=False
                    ).exists()
                ):
                    orderwsa = OrderWorkStaffAssign.objects.filter(
                        staff=staff, assign_date_time__isnull=False
                    ).values_list('id')
                    ordertaken = OrderWorkStaffTaken.objects.filter(orderworkstaffassign_id__in = orderwsa,
                        taken_date_time__isnull=True
                    )
                    serializer = OrderWorkStaffTakenSerializers(ordertaken, many=True)
                    return Response(
                        {"data": serializer.data, "status": True, "message": "Success"},
                        status.HTTP_200_OK,
                    )

                else:
                    return Response(
                        {"status": False, "message": "Failure"}, status.HTTP_200_OK
                    )
            except Exception as e:
                resp = KeyErrorContext(False, "Failed", str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False, "Failed", "key missmatch")
            return Response(resp)

    elif request.method == "GET":
        orders = OrderWorkStaffAssign.objects.all()
        serializer = OrderWorkStaffAssignSerializers(orders, many=True)
        return Response(
            {"data": serializer.data, "status": True, "message": "Success"},
            status.HTTP_200_OK,
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def staff_work_taken(request):
    if request.method == "POST":
        data = request.data
        keys = "staff_id"
        if (i in data for i in keys):
            staff_id = data["staff_id"]
            try:
                staff = fetchStaff(staff_id)

                if OrderWorkStaffTaken.objects.filter(
                    orderworkstaffassign__staff_id=staff.staff_id
                ).exists():

                    ordertaken = OrderWorkStaffTaken.objects.exclude(
                        orderworkstaffassign__staff_id=staff.staff_id,
                        taken_date_time__isnull=True,
                    ).filter(staff = staff)
                    serializer = OrderWorkStaffTakenSerializers(ordertaken, many=True)

                    return Response(
                        {"data": serializer.data, "status": True, "message": "Success"},
                        status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"status": False, "message": "Failed"}, status.HTTP_200_OK
                    )
            except Exception as e:
                resp = KeyErrorContext(False, "Failed", str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False, "Failed", "key missmatch")
            return Response(resp)

    elif request.method == "GET":

        orders = OrderWorkStaffAssign.objects.all()
        serializer = OrderWorkStaffAssignSerializers(orders, many=True)
        return Response(
            {"data": serializer.data, "status": True, "message": "Success"},
            status.HTTP_200_OK,
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def staff_work_take(request):
    if request.method == "POST":
        data = request.data

        keys = ("staff_id", "order_id", "work_id", "assigned_stage", "order_work_label")
        if (i in data for i in keys):
            staff_id = data["staff_id"]
            order_id = data["order_id"]
            work_id = data["work_id"]
            assigned_stage = data["assigned_stage"]
            order_work_label = data["order_work_label"]
            try:
                order = fetchOrder(order_id)
                work = fetchWork(work_id)
                staff = fetchStaff(staff_id)

                if OrderWorkStaffAssign.objects.filter(
                    order=order, order_work_label=order_work_label
                ).exists():
                    ordw = OrderWorkStaffAssign.objects.filter(
                        order=order, order_work_label=order_work_label
                    ).last()
                    OrderWorkStaffTaken.objects.filter(
                        orderworkstaffassign=ordw
                    ).update(taken_date_time=datetime.datetime.now())

                    if OrderWorkStaffStatusCompletion.objects.filter(
                        order=order, staff=staff, orderworkstaffassign=ordw
                    ).exists():
                        return Response(
                            {
                                "status": True,
                                "message": "Success",
                                "details": "Order already taken",
                            }
                        )
                    else:
                        OrderWorkStaffStatusCompletion.objects.create(
                            order=order,
                            staff=staff,
                            orderworkstaffassign=ordw,
                            work_staff_completion_stage=assigned_stage,
                        )
                        return Response(
                            {
                                "status": True,
                                "message": "Success",
                                "details": "Order taken",
                            }
                        )
                else:
                    return Response(
                        {
                            "status": True,
                            "message": "Success",
                            "details": "order work already staff taken",
                        }
                    )
            except Exception as e:
                resp = KeyErrorContext(False, "Failed", str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False, "Failed", "key missmatch")
            return Response(resp)

    elif request.method == "GET":

        orders = OrderWorkStaffAssign.objects.all()
        serializer = OrderWorkStaffAssignSerializers(orders, many=True)
        return Response(
            {"data": serializer.data, "status": True, "message": "Success"},
            status.HTTP_200_OK,
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def staff_work_assign_completion(request):
    if request.method == "POST":
        data = request.data
        keys = "staff"
        if (i in data for i in keys):
            try:
                staff_id = data["staff"]
                staff = fetchStaff(staff_id)

                if (
                    OrderWorkStaffStatusCompletion.objects.exclude(
                        work_completed_date_time__isnull=False
                    )
                    .filter(staff=staff)
                    .exists()
                ):
                    ordc = OrderWorkStaffStatusCompletion.objects.exclude(
                        work_completed_date_time__isnull=False
                    ).filter(staff=staff)
                    serializer = OrderWorkStaffAssignCompletionSerializers(
                        ordc, many=True
                    )
                    return Response(
                        {"data": serializer.data, "status": True, "message": "Success"},
                        status.HTTP_200_OK,
                    )
                else:
                    return Response({"status": False, "message": "not found"})

            except Exception as e:
                resp = KeyErrorContext(False, "Failed", str(e))
                return Response(resp)
        else:
            return Response(
                {"status": False, "message": "Failed", "error": "key missmatch"}
            )
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def staff_work_completion_review(request):
    if request.method == "POST":
        data = request.data
        keys = "staff"
        if (i in data for i in keys):
            try:
                staff_id = data["staff"]
                staff = fetchStaff(staff_id)

                if (
                    OrderWorkStaffStatusCompletion.objects.exclude(
                        work_completed_date_time__isnull=True
                    )
                    .exclude(work_staff_completion_approved=True)
                    .filter(staff=staff)
                    .exists()
                ):
                    ordc = OrderWorkStaffStatusCompletion.objects.exclude(
                        work_completed_date_time__isnull=True
                    ).exclude(work_staff_completion_approved=True)
                    serializer = OrderWorkStaffAssignCompletionSerializers(
                        ordc, many=True
                    )
                    return Response(
                        {"data": serializer.data, "status": True, "message": "Success"},
                        status.HTTP_200_OK,
                    )
                else:
                    return Response({"status": False, "message": "not found"})

            except Exception as e:
                resp = KeyErrorContext(False, "Failed", str(e))
                return Response(resp)
        else:
            return Response(
                {"status": False, "message": "Failed", "error": "key missmatch"}
            )
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def staff_stage_completion(request):
    if request.method == "POST":
        data = request.data
        keys = ("staff_id", "order_id", "work_id", "stage", "order_work_label")
        if (i in data for i in keys):
            try:
                staff_id = data["staff_id"]
                order_id = data["order_id"]
                work_id = data["work_id"]
                stage = data["stage"]
                order_work_label = data["order_work_label"]

                order = fetchOrder(order_id)
                staff = fetchStaff(staff_id)

                orderwa = OrderWorkStaffAssign.objects.get(
                    order_work_label=order_work_label,assign_stage = stage
                )

                if OrderWorkStaffStatusCompletion.objects.filter(
                    staff=staff, order=order, orderworkstaffassign=orderwa
                ).exists():
                    ordc = OrderWorkStaffStatusCompletion.objects.filter(
                        staff=staff, order=order, orderworkstaffassign=orderwa
                    ).update(work_completed_date_time=datetime.datetime.now())
                    return Response({"status": True, "message": "Success"})
                else:
                    return Response({"status": False, "message": "not found"})

            except Exception as e:
                resp = KeyErrorContext(False, "Failed", str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False, "Failed", "key missmatch")
            return Response(resp)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def staff_work_assign_completion_app(request):
    if request.method == "POST":
        data = request.data
        keys = ("staff_id", "order_id", "work_id", "stage", "state", "order_work_label")
        if (i in data for i in keys):
        
            staff_id = data["staff_id"]
            order_id = data["order_id"]
            work_id = data["work_id"]
            stage = data["stage"]
            state = data["state"]

            order_work_label = data["order_work_label"]

            order = fetchOrder(order_id)
            work = fetchWork(work_id)
            print(work)
            staff = fetchStaff(staff_id)

            orderwa = OrderWorkStaffAssign.objects.get(
                order_work_label=order_work_label,
                assign_stage = stage,
                staff=staff,
            )

            if state == "approve":
                if OrderWorkStaffStatusCompletion.objects.filter(
                    staff=staff, order=order, orderworkstaffassign=orderwa
                ).exists():
                    ordc = OrderWorkStaffStatusCompletion.objects.filter(
                        staff=staff, order=order, orderworkstaffassign=orderwa
                    ).update(
                        work_staff_comp_app_date_time=datetime.datetime.now(),
                        work_staff_completion_approved=True,
                    )
                    OrderWorkStaffAssign.objects.create(
                        order=order,
                        work=work,
                        order_work_label=orderwa.order_work_label,
                        staff=None,
                    )
                    resp = SuccessContext(True, "Success", "Updated")
                    return Response(resp)
                else:
                    resp = SuccessContext(True, "Success", "Already Updated")
                    return Response(resp)
            elif state == "reassign":
                OrderWorkStaffStatusCompletion.objects.filter(
                    staff=staff, order=order
                ).delete()
                orderworkstaffassign = OrderWorkStaffAssign.objects.get(
                    order=order,
                    work=work,
                    assign_stage=stage,
                    order_work_label=orderwa.order_work_label,
                )
                OrderWorkStaffTaken.objects.filter(
                    orderworkstaffassign=orderworkstaffassign, taken_stage=stage
                ).delete()
                OrderWorkStaffAssign.objects.filter(
                    order=order,
                    work=work,
                    order_work_label=orderwa.order_work_label,
                ).update(staff=None, assign_stage=None, assign_date_time=None)
                OrderWorkStaffAssign.objects.filter(
                    order=order,
                    work=work,
                    assign_stage=stage,
                    order_work_label=orderwa.order_work_label,
                ).update(staff=None, assign_stage=None, assign_date_time=None)
                resp = SuccessContext(True, "Success", "deleted")
                return Response(resp)

            # except Exception as e:
            #     resp = KeyErrorContext(False, "Failed", str(e))
            #     return Response(resp)
        else:
            resp = KeyErrorContext(False, "Failed", "key missmatch")
            return Response(resp)
    else:
        if OrderWorkStaffStatusCompletion.objects.filter(
            work_staff_completion_approved=False, work_completed_date_time__isnull=False
        ).exists():
            ordc = OrderWorkStaffStatusCompletion.objects.filter(
                work_staff_completion_approved=False,
                work_completed_date_time__isnull=False,
            )
            serializer = OrderWorkStaffAssignCompletionSerializers(ordc, many=True)
            return Response(
                {"data": serializer.data, "status": True, "message": "Success"},
                status.HTTP_200_OK,
            )
        else:
            return Response({"status": False, "message": "Success"}, status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET", "POST"])
# def work_finalize(request):
#     if request.method == "POST":
#         data = request.data
#         keys = ("staff_id", "order_id", "work_id", "stage", "date")
#         if (i in data for i in keys):
#             try:
#                 staff_id = data["staff_id"]
#                 order_id = data["order_id"]
#                 work_id = data["work_id"]
#                 stage = data["stage"]
#                 date = data["date"]

#                 order = fetchOrder(order_id)
#                 work = fetchWork(work_id)
#                 staff = fetchStaff(staff_id)

#                 if OrderWorkStaffStatusCompletion.objects.filter(
#                     staff=staff, order=order, work_staff_completion_approved=True
#                 ).exists():
#                     ordc = OrderWorkStaffStatusCompletion.objects.filter(
#                         staff=staff, order=order, work_staff_completion_approved=True
#                     ).update(order_next_stage_assign=True)
#                     OrderWorkStaffAssign.objects.create(
#                         order=order, work=work, staff=None
#                     )
#                     resp = SuccessContext(True, "Success", "Work finished")
#                     return Response(resp)
#                 else:
#                     resp = SuccessContext(True, "Failure", "not allowed")
#                     return Response(resp)

#             except Exception as e:
#                 resp = KeyErrorContext(False, "Failed", str(e))
#                 return Response(resp)
#         else:
#             resp = KeyErrorContext(False, "Failed", "key missmatch")
#             return Response(resp)
#     elif request.method == "GET":
#         if OrderWorkStaffStatusCompletion.objects.filter(
#             work_staff_completion_approved=True, order_next_stage_assign=False
#         ).exists():
#             ordc = OrderWorkStaffStatusCompletion.objects.filter(
#                 work_staff_completion_approved=True, order_next_stage_assign=False
#             )
#             serializer = OrderWorkStaffAssignCompletionSerializers(ordc, many=True)
#             return Response(
#                 {"data": serializer.data, "status": True, "message": "Success"},
#                 status.HTTP_200_OK,
#             )
#         else:
#             return Response({"status": False, "message": "Success"}, status.HTTP_200_OK)
#     return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def staff_work_assign_completion_approval(request):
#     if request.method == "POST":
#         data = request.data
#         keys = ("id", "order_id", "staff_id", "work_id")
#         if (i in data for i in keys):
#             try:
#                 ids = int(data["id"])

#                 approval = True
#                 assignnextstage = True
#                 staff_id = data["staff_id"]
#                 order_id = data["order_id"]

#                 staff = fetchStaff(staff_id)
#                 order = fetchOrder(order_id)

#                 if OrderWorkStaffStatusCompletion.objects.filter(
#                     id=ids, work_staff_completion_approved=True
#                 ).exists():
#                     return Response(
#                         {
#                             "status": True,
#                             "message": "Success",
#                             "details": "Order already approved",
#                         }
#                     )
#                 else:
#                     orderworkstaffstatuscompletion = (
#                         OrderWorkStaffStatusCompletion.objects.get(id=ids)
#                     )
#                     orderworkstaffstatuscompletion.work_staff_completion_approved = (
#                         approval
#                     )
#                     orderworkstaffstatuscompletion.order_next_stage_assign = (
#                         assignnextstage
#                     )
#                     orderworkstaffstatuscompletion.save()

#                     StaffWorkWage.objects.create(
#                         order=order,
#                         staff=staff,
#                         orderworkstatuscompletion=orderworkstaffstatuscompletion,
#                     )

#                     return Response(
#                         {
#                             "status": True,
#                             "message": "Success",
#                             "details": "Order approved",
#                         }
#                     )
#             except Exception as e:
#                 resp = KeyErrorContext(False, "Failed", str(e))
#                 return Response(resp)
#         else:
#             resp = KeyErrorContext(False, "Failed", "key missmatch")
#             return Response(resp)
#     return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "PUT"])
def staff_wage_calculation(request):
    if request.method == "POST":
        data = request.data
        keys = "staff_id"
        if (i in data for i in keys):
            staff_id = data["staff_id"]
            try:
                staff = fetchStaff(staff_id)
                if staff.salary_type == "monthly":
                    pass
                elif staff.salary_type == "wage":
                    if StaffWorkWage.objects.filter(
                        staff=staff, wage_given=False
                    ).exists():
                        works = OrderWorkStaffStatusCompletion.objects.filter(
                            staff=staff, work_staff_completion_approved=True
                        )
                        for work in works:
                            if work.orderworkstaffassign.work.wage_type == "full":
                                amount = work.orderworkstaffassign.work.amount
                                StaffWorkWage.objects.filter(
                                    staff=staff,
                                    wage_given=False,
                                    work=work.orderworkstaffassign.work,
                                ).update(wage=amount)
                            elif work.orderworkstaffassign.work.wage_type == "half":
                                amount = work.orderworkstaffassign.work.amount / 2
                                StaffWorkWage.objects.filter(
                                    staff=staff,
                                    wage_given=False,
                                    work=work.orderworkstaffassign.work,
                                ).update(wage=amount)
                            elif work.orderworkstaffassign.work.wage_type == "10half":
                                amount = (
                                    work.orderworkstaffassign.work.amount - 10
                                ) / 2
                                StaffWorkWage.objects.filter(
                                    staff=staff,
                                    wage_given=False,
                                    work=work.orderworkstaffassign.work,
                                ).update(wage=amount)
                            else:
                                pass
                    else:
                        pass
                else:
                    return Response(
                        {
                            "status": False,
                            "message": "Failed",
                            "error": "please fill staff details",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                staffwages = StaffWorkWage.objects.filter(staff=staff)
                serializer = StaffWorkWageSerializers(staffwages, many=True)
                return Response(
                    {"data": serializer.data, "status": True, "message": "Success"},
                    status.HTTP_200_OK,
                )
            except Exception as e:
                resp = KeyErrorContext(False, "Failed", str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False, "Failed", "key missmatch")
            return Response(resp)

    if request.method == "PUT":
        data = request.data
        keys = ("from_date", "to_date", "payment_date", "staff_id", "ids", "w_total")
        if (i in data for i in keys):
            staff_id = json.loads(data["staff_id"])
            ids = json.loads(data["ids"])
            from_date = data["from_date"]
            payment_date = data["payment_date"]
            payment_ref = json.loads(data["payment_ref"])
            to_date = data["to_date"]
            payment_ref_image = request.FILES.get("file")
            w_total = json.loads(data["w_total"])

            try:

                f_date = datetime.datetime.strptime(
                    from_date[1:11], "%d/%m/%Y"
                ).strftime("%Y-%m-%d")
                t_date = datetime.datetime.strptime(to_date[1:11], "%d/%m/%Y").strftime(
                    "%Y-%m-%d"
                )
                staff_id = fetchStaff(staff_id)
                if StaffWageGivenStatus.objects.filter(
                    staff=staff_id,
                    order_ids=ids,
                    wage_from_date=f_date,
                    wage_to_date=t_date,
                    total_wage_given=w_total,
                ).exists():
                    return Response({"status": False, "message": "Failure"})
                else:
                    StaffWageGivenStatus.objects.create(
                        staff=staff_id,
                        order_ids=ids,
                        wage_from_date=f_date,
                        wage_to_date=t_date,
                        total_wage_given=w_total,
                        wage_payment_reference_no=payment_ref,
                        wage_payment_reference_image=payment_ref_image,
                    )
                    for id in ids:
                        StaffWorkWage.objects.filter(id=id).update(
                            completion_date_time=datetime.datetime.now(),
                            wage_given=True,
                        )

                    return Response(
                        {"status": True, "message": "Success"},
                        status=status.HTTP_201_CREATED,
                    )
            except Exception as e:
                resp = KeyErrorContext(False, "Failed", str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False, "Failed", "key missmatch")
            return Response(resp)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def pending_wage(request):
    if request.method == "POST":
        data = request.data
        keys = "staff_id"
        if (i in data for i in keys):
            staff_id = data["staff_id"]
            try:
                staff = fetchStaff(staff_id)
                staffwages = StaffWorkWage.objects.filter(staff=staff, wage_given=False)
                serializer = StaffWorkWageSerializers(staffwages, many=True)
                if serializer.data:
                    return Response(
                        {"data": serializer.data, "status": True, "message": "Success"},
                        status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"data": [], "status": False, "message": "Success"},
                        status.HTTP_200_OK,
                    )
            except Exception as e:
                resp = KeyErrorContext(False, "Failed", str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False, "Failed", "key missmatch")
            return Response(resp)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET','POST'])
# def staff_wage_manager(request):
#     if request.method == "POST":
#         data = request.data
#         keys = ('staff_id')
#         if (i in data for i in keys):
#             staff_id = data['staff_id']
#             try:
#                 staff = fetchStaff(staff_id)
#                 staffwages = StaffWorkWage.objects.filter(staff = staff)
#                 serializer = StaffWorkWageSerializers(staffwages,many=True)
#                 return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK)
#             except Exception as e:
#                 resp = KeyErrorContext(False,'Failed',str(e))
#                 return Response(resp)
#         else:
#             resp = KeyErrorContext(False,'Failed','key missmatch')
#             return Response(resp)

#     elif request.method == 'GET':
#         staffwages = StaffWorkWage.objects.all()
#         serializer = StaffWorkWageSerializers(staffwages,many=True)
#         return Response({"data":serializer.data,"status":True,"message":"Success"},status.HTTP_200_OK)
#     return Response(serializers.data,status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def staff_payment_update(request):
    if request.method == "POST":
        data = request.data
        keys = ("staff_id", "id", "dates")
        if all(i in data for i in keys):
            id = data["id"]
            staff_id = data["staff_id"]
            dates = data["dates"]

            staff = fetchStaff(staff_id)
            total = StaffWorkWage.objects.filter(
                staff=staff, wage_given=False, id__in=id
            ).aggregate(Sum("wage"))
            return Response(
                {
                    "data": total,
                    "from_date": dates[0],
                    "to_date": dates[-1],
                    "status": True,
                    "message": "Success",
                },
                status.HTTP_200_OK,
            )
        else:
            resp = KeyErrorContext(False, "Failed", "key missmatch")
            return Response(resp)
    return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def staff_wage_paid_completion(request):
    if request.method == "POST":
        data = request.data
        if (i in data for i in keys):
            staff_id = data["staff_id"]
            try:
                if StaffWageGivenStatus.objects.filter(
                    staff=staff_id,
                    order_ids=ids,
                    wage_from_date=f_date,
                    wage_to_date=t_date,
                    total_wage_given=w_total,
                ).exists():
                    return Response(
                        {"data": serializer.data, "status": True, "message": "Success"},
                        status=status.HTTP_200_OK,
                    )

                else:

                    return Response(
                        {"data": [], "status": False, "message": "Success"},
                        status=status.HTTP_200_OK,
                    )
            except Exception as e:
                resp = KeyErrorContext(False, "Failed", str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False, "Failed", "key missmatch")
            return Response(resp)
    else:
        staffworkwage = StaffWorkWage.objects.filter(wage_given=True)
        serializer = StaffWorkWageSerializers(staffworkwage, many=True)
        if serializer.data:
            return Response(
                {"data": serializer.data, "status": True, "message": "Success"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"data": [], "status": False, "message": "Success"},
                status=status.HTTP_200_OK,
            )
    return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def staff_wage_status(request, status):
    if request.method == "POST" and status == "paid":
        data = request.data
        staff_id = data["staff_id"]
        staff_id = fetchStaff(staff_id)
        staffworkwage = StaffWorkWage.objects.filter(staff = staff_id,wage_given__isnull = False)
        serializer = StaffWorkWageSerializers(staffworkwage,many = True)
        if serializer.data:
            return Response(
                {"data": serializer.data, "status": True, "message": "Success"}
            )
        else:
            return Response({"data": [], "status": False, "message": "Success"})

    elif request.method == "POST" and status == "notpaid":
        data = request.data
        staff_id = data["staff_id"]
        staff_id = fetchStaff(staff_id)
        staffworkwage = StaffWorkWage.objects.filter(staff = staff_id,wage_given__isnull = True)
        serializer = StaffWorkWageSerializers(staffworkwage,many = True)
        if serializer.data:
            return Response(
                {"data": serializer.data, "status": True, "message": "Success"}
            )
        else:
            return Response({"data": [], "status": False, "message": "Success"})
    return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderWorkStaffAssignView(APIView):
    def get(self, request):
        model = OrderWorkStaffAssign.objects.all()
        serializer = OrderWorkStaffAssignSerializer(model, many=True)
        return Response(serializer.data)

    def get(self, order_id):
        model = OrderWorkStaffAssign.objects.filter(order_id=order_id)
        serializer = OrderWorkStaffAssignSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        keys = ("order_id", "work_id", "order_work_label")
        if all(i in data for i in keys):

            try:
                order = Order.objects.get(order_id=data["order_id"])
                work = Work.objects.get(work_id=data["work_id"])
                order_work_label = data["order_work_label"]
                OrderWorkStaffAssign.objects.create(
                    order=order,
                    work=work,
                    order_work_label=order_work_label,
                    staff=None,
                ).save()
                return Response(
                    {"status": True, "message": "Inserted"},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"status": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def delete(self, request):
        data = request.data
        if "order_id" in data:
            order = Order.objects.get(order_id=data["order_id"])
            try:
                OrderWorkStaffAssign.objects.get(order=order).delete()
            except Exception as e:
                return Response(
                    {"status": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def put(self, request):
        data = request.data
        keys = ("order_id", "work_id", "staff_id", "assign_stage", "assign_date_time")
        if all(i in data for i in keys):
            order = Order.objects.get(order_id=data["order_id"])
            work = Work.objects.get(work_id=data["work_id"])
            staff = Staff.objects.get(staff_id=data["staff_id"])
            try:
                OrderWorkStaffAssign.objects.get(order=order, assign_stage="").update(
                    order=order,
                    work=work,
                    staff=staff,
                    assign_stage=data["assign_stage"],
                    assign_date_time=data["assign_date_time"],
                )
                return Response(
                    {"status": True, "message": "Updated"},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"status": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class StaffWorkWageView(APIView):
    def post(self, request):
        data = request.data
        keys = ("order_id", "staff_id", "work_id")
        if all(i in data for i in keys):
            staff = Staff.objects.get(staff_id=data["staff_id"])
            order = Order.objects.get(order_id=data["order_id"])
            work = Work.objects.get(work=data["work"])
            try:
                StaffWorkWage.objects.create(
                    staff=staff,
                    order=order,
                    work=work,
                    work_staff_approval_date_time=None,
                    completion_date_time=None,
                    wage=None,
                    wage_given=None,
                ).save()
                return Response(
                    {"status": True, "message": "Inserted"},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"status": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def delete(self, request):
        data = request.data
        if "id" in data:
            id = data["id"]
            try:
                StaffWorkWage.objects.get(id=id).delete()
                return Response(
                    {"status": True, "message": "Deleted"},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"status": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class StaffWageGivenStatusView(APIView):
    def post(self, request):
        data = request.data
        keys = ("order_id", "staff_id", "work_id")
        if all(i in data for i in keys):
            staff = Staff.objects.get(staff_id=data["staff_id"])
            order = Order.objects.get(order_id=data["order_id"])
            work = Work.objects.get(work=data["work"])
            try:
                StaffWageGivenStatus.objects.create(
                    staff=staff,
                    order=order,
                    work=work,
                    wage_from_date=None,
                    wage_to_date=None,
                    wage_given_date=None,
                    total_wage_given=None,
                    wage_payment_reference_no=None,
                    wage_payment_reference_image=None,
                ).save()
                return Response(
                    {"status": True, "message": "Inserted"},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"status": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def delete(self, request):
        data = request.data
        if "id" in data:
            id = data["id"]
            try:
                StaffWageGivenStatus.objects.get(id=id).delete()
                return Response(
                    {"status": True, "message": "Deleted"},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"status": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )


@api_view(["POST"])
def get_details(request):
    if request.method == "POST":
        data = request.data
        try:
            login_id = data["login_id"]
            if User.objects.filter(login_id=login_id).exists():
                auth = User.objects.filter(login_id=login_id).last()
                user = UserSerializer(auth)
                if auth.role == "staff":
                    staff = Staff.objects.get(staff_id=auth.login_id)
                    serializer = StaffSerializer(staff)
                    return Response(
                        {
                            "status": True,
                            "message": "Success",
                            "data": serializer.data,
                            "user": user.data,
                        }
                    )
                elif auth.role == "customer":
                    customer = Customer.objects.get(cust_id=auth.login_id)
                    serializer = CustomerSerializer(customer)
                    return Response(
                        {
                            "status": True,
                            "message": "Success",
                            "data": serializer.data,
                            "user": user.data,
                        }
                    )
                elif auth.role == "admin":
                    return Response(
                        {"status": True, "message": "Success", "user": user.data}
                    )
                else:
                    return Response({"status": False, "message": "Failed"})

        except Exception as e:
            resp = KeyErrorContext(False, "Failed", str(e))
            return Response(resp)

    return Response(
        {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET", "POST"])
def upload_file(request):

    name = request.POST["name"]
    file = request.FILES["file"]
    print(file)

    try:
        UploadFile.objects.create(name=name, file=file)
        return Response(
            {"status": True, "message": "Inserted"}, status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def work_completed(request):
    if request.method == "POST":
        data = request.data
        keys = ("staff_id",)
        if all(i in data for i in keys):
            staff_id = data["staff_id"]
            try:
                staff = fetchStaff(staff_id)
                if OrderWorkStaffStatusCompletion.objects.filter(
                    staff=staff, work_staff_completion_approved=True
                ).exists():
                    ordersc = OrderWorkStaffStatusCompletion.objects.filter(
                        staff=staff, work_staff_completion_approved=True
                    )
                    serializer = OrderWorkStaffAssignCompletionSerializers(
                        ordersc, many=True
                    )
                    return Response(
                        {"status": True, "message": "Success", "data": serializer.data}
                    )
                else:
                    return Response(
                        {"status": False, "message": "Failure", "details": "Not found"}
                    )
            except Exception as e:
                resp = KeyErrorContext(False, "Failed", str(e))
                return Response(resp)
        else:
            resp = KeyErrorContext(False, "Failed", "key missmatch")
            return Response(resp)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class MaterialLocationView(APIView):
    def get(self, request, orderid):
        model = OrderMaterialLocation.objects.filter(order__order_id=orderid)
        serializer = OrderMaterialLocationSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        keys = ("order_id", "staff_id", "material_location")
        if all(i in data for i in keys):
            order_id = data["order_id"]
            staff_id = data["staff_id"]
            material_location = data["material_location"]

            try:
                OrderMaterialLocation.objects.create(
                    order_id=order_id,
                    staff_id=staff_id,
                    material_location=material_location,
                )
                return Response({"status": True, "message": "Inserted"})
            except Exception as e:
                return Response({"status": False, "message": str(e)})
        else:
            return Response({"status": False, "message": "Key Missmatch"})


@api_view(["POST"])
def order_status_from_order_assign(request):
    if request.method == "POST":
        data = request.data
        if "order_id" in data:
            order_id = data["order_id"]
            osa = OrderWorkStaffStatusCompletion.objects.filter(
                order_id=order_id,
                order_next_stage_assign=False,
            ).order_by("-work_staff_comp_app_date_time")
            serializer = OrderWorkStaffAssignCompletionSerializers(osa, many=True)
            return Response(
                {
                    "data": serializer.data,
                }
            )
        else:
            return Response({"data": []})


@api_view(["GET", "POST"])
def order_status_admin(request):
    if request.method == "POST":
        data = request.data
        if "order_id" in data:
            # cust_id = data['cust_id']
            order_id = data["order_id"]
            order = fetchOrder(order_id)
            try:
                ords = OrderWorkStaffStatusCompletion.objects.filter(
                    order=order,
                    work_staff_completion_approved=True,
                ).order_by("-work_staff_comp_app_date_time")

                include_res = []
                for i in ords:
                    exclude_list = [
                        "cutting",
                        "stitching",
                        "hook",
                        "overlock",
                        "Completed",
                    ]

                    if i.work_staff_completion_stage in exclude_list:
                        exclude_list.remove(i.work_staff_completion_stage)
                        include_res.append(
                            {
                                "stage": i.work_staff_completion_stage,
                                "staff_name": i.staff.staff_name,
                                "completion_date_time": i.work_completed_date_time,
                                "status": True,
                            }
                        )
                    else:
                        pass

                    try:
                        for e in exclude_list:
                            include_res.append({"stage": e, "status": False})
                    except:
                        pass

                resp = SuccessContext(True, "Success", include_res)
                return Response(resp)
            except Exception as e:
                return Response(
                    {"data": [], "status": False, "message": "Failed", "error": str(e)}
                )
        else:
            return Response(
                {
                    "data": [],
                    "status": False,
                    "message": "Failed",
                    "error": "key missmatch",
                }
            )
    return Response({"GET": "Not Allowed"})


@api_view(["POST"])
def order_status_from_order_assign_admin(request):
    if request.method == "POST":
        data = request.data
        if "order_id" in data:
            order_id = data["order_id"]
            osa = OrderWorkStaffStatusCompletion.objects.filter(
                order_id=order_id,
                order_next_stage_assign=False,
            ).order_by("-work_staff_comp_app_date_time")
            serializer = OrderWorkStaffAssignCompletionSerializers(osa, many=True)
            return Response(
                {"data": serializer.data, "status": True, "message": "Success"}
            )
        else:
            return Response({"data": [], "status": False, "message": "Failed"})


class AdminOrder(APIView):
    def get(self, request):
        model = OrderWorkStaffAssign.objects.filter(assign_stage__isnull=False)
        serializer = OrderWorkStaffAssignSerializer(model, many=True)
        return Response(serializer.data)


class CustomerOrder(APIView):
    def get(self, request, custid):
        customer = Customer.objects.get(cust_id=custid)
        orders = Order.objects.filter(customer=customer).values_list("order_id")
        ord_as = OrderWork.objects.filter(order_id__in=orders)
        # print(ord_as.annotate(Count("order_id")))
        serializer = OrderWorkSerializer(ord_as, many=True)
        return Response(serializer.data)


class OrderInvoiceView(APIView):
    def post(self, request):
        keys = ("order_id", "cust_id")
        data = request.data
        if all(i in data for i in keys):
            order_id = data["order_id"]
            cust_id = data["cust_id"]

            try:
                # get (TOTAL,ADVANCE,BALACE) from Order
                orders = Order.objects.filter(
                    order_id=order_id, customer__cust_id=cust_id
                )
                serialized_order = OrderSerializer(orders, many=True)

                # get (WORK_NAME,QUANTITY,PRICE,AMOUTN/ITEM)
                order_work = OrderWork.objects.filter(order_id=order_id)
                serialized_order_work = OrderWorkSerializer(order_work, many=True)

                # get (MATERIAL_NAME,QUANTITY,PRICE,AMOUNT/ITEM)
                order_material = OrderMaterial.objects.filter(order_id=order_id)
                serialized_order_material = OrderMaterialSerializer(
                    order_material, many=True
                )
                return Response(
                    {
                        "status": True,
                        "order": serialized_order.data,
                        "order_work": serialized_order_work.data,
                        "order_material": serialized_order_material.data,
                    }
                )

            except Exception as e:
                return Response({"status": False, "message": str(e)})
        return Response({"status": False, "message": "key error"})


class ProductView(APIView):
    def get(self, request):
        model = Product.objects.all()
        serializer = ProductSerializer(model, many=True)
        return Response({"status": True, "data": serializer.data})

    def post(self, request):
        data = json.loads(request.POST["data"])
        try:
            product_name, display, new_arrival, picture = (
                "",
                False,
                False,
                request.FILES.get("picture"),
            )

            product_id = "ZP" + str(randint(9999, 100000))
            print(product_id)
            if "product_name" in data:
                product_name = data["product_name"]
            if "display" in data:
                display = data["display"]
            if "new_arrival" in data:
                new_arrival = data["new_arrival"]
            if "picture" in data:
                picture = request.FILES.get("picture")

            Product.objects.create(
                product_id=product_id,
                product_name=product_name,
                display=display,
                new_arrival=new_arrival,
                picture=picture,
            ).save()

            print(data["display"], data["new_arrival"], display, new_arrival, picture)

            return Response(
                {"status": True, "message": "Success"}, status.HTTP_201_CREATED
            )
            # return Response(
            #     {"status": False, "message": "Image Requried"},
            #     status.HTTP_204_NO_CONTENT,
            # )
        except Exception as e:
            return Response(
                {"status": False, "message": str(e)},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, productid):
        data = json.loads(request.POST["data"])
        try:
            product = Product.objects.get(product_id=productid)
            product_name, display, new_arrival = (
                "",
                False,
                False,
            )
            if "product_name" in data:
                product_name = data["product_name"]
                product.product_name = product_name
            if "display" in data:
                display = data["display"]
                product.display = display
            if "new_arrival" in data:
                new_arrival = data["new_arrival"]
                product.new_arrival = new_arrival
            if "picture" in data:
                picture = request.FILES.get("picture")
                if picture is not None:
                    product.picture = picture
            print(data["display"], data["new_arrival"], display, new_arrival, picture)
            product.save()

            return Response(
                {"status": True, "message": "Success"}, status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"status": False, "message": str(e)},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, productid):
        try:
            Product.objects.filter(product_id=productid).delete()
            return Response({"status": True, "message": "Deleted"})
        except Exception as e:
            return Response({"status": False, "data": [], "message": str(e)})


@api_view(["GET"])
def get_product(request):
    try:
        model = Product.objects.get(product_id=request.GET.get("pid"))
        serializer = ProductSerializer(model)
        return Response({"status": True, "data": serializer.data})
    except Exception as e:
        return Response({"status": True, "data": [], "message": str(e)})


@api_view(["GET"])
def new_arrivals(request):
    if request.method == "GET":
        model = Product.objects.filter(new_arrival=True).order_by('created_at')[:3]
        serializer = ProductSerializer(model, many=True)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["GET"])
def product_to_display(request):
    if request.method == "GET":
        model = Product.objects.filter(display=True).order_by('created_at')[:6]
        serializer = ProductSerializer(model, many=True)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["GET"])
def get_products(request):
    if request.method == "GET":
        model = Product.objects.all()
        serializer = ProductSerializer(model, many=True)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["GET"])
def ready_to_delivery(request):
    if request.method == "GET":
        model = Delivery.objects.filter(staff=None)
        serializer = DeliverySerializer(model, many=True)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["GET"])
def customers(request):
    customer = Customer.objects.all()
    serializer = CustomerSerializer(customer, many=True)
    if serializer.data:
        return Response(serializer.data)
    else:
        return Response([], status=status.HTTP_404_NOT_FOUND)


# CUSTOMER PENDING ORDERS
@api_view(["POST"])
def customer_pending_orders(request):
    data = request.data
    print(data)
    if "login_id" in data:
        login_id = data["login_id"]
        customer = fetchCustomer(login_id)
        order_id = Order.objects.filter(customer=customer).values_list("order_id")
        orders = (
            OrderWorkStaffAssign.objects.filter(order_id__in=order_id)
            .exclude(assign_stage="complete_final_stage")
            .count()
        )
        return Response(orders)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# CUSTOMER COMPLETED ORDERS
@api_view(["POST"])
def customer_completed_orders(request):
    data = request.data
    if data["login_id"]:
        login_id = data["login_id"]
        customer = fetchCustomer(login_id)
        order_id = Order.objects.filter(customer=customer).values_list("order_id")
        orders = (
            OrderWorkStaffAssign.objects.filter(order_id__in=order_id)
            .filter(assign_stage="complete_final_stage")
            .count()
        )
        return Response(orders)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# CUSTOMER TOTAL ORDERS
@api_view(["POST"])
def customer_total_orders(request):
    data = request.data
    if data["login_id"]:
        login_id = data["login_id"]
        customer = fetchCustomer(login_id)
        order_id = Order.objects.filter(customer=customer).values_list("order_id")
        orders = OrderWorkStaffAssign.objects.filter(order_id__in=order_id).count()
        return Response(orders)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# CUSTOMER  DELIVERY READY
@api_view(["POST"])
def customer_delivery_ready(request):
    data = request.data
    if data["login_id"]:
        login_id = data["login_id"]
        customer = fetchCustomer(login_id)
        order_id = Order.objects.filter(customer=customer).values_list("order_id")
        delivery_ready = Delivery.objects.filter(
            delivery_date_time__isnull=True, order_id__in=order_id
        ).count()
        return Response(delivery_ready)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# STAFF TOTAL WORKS
@api_view(["POST"])
def staff_total_works(request):
    data = request.data
    if data["login_id"]:
        login_id = data["login_id"]
        staff = fetchStaff(login_id)
        works = OrderWorkStaffAssign.objects.filter(staff=staff).values_list("id")
        totalworks = OrderWorkStaffTaken.objects.filter(id__in=works).count()
        return Response(totalworks)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# STAFF ASSIGNED WORKS
@api_view(["POST"])
def staff_not_taken_works(request):
    data = request.data
    if data["login_id"]:
        login_id = data["login_id"]
        staff = fetchStaff(login_id)
        works = OrderWorkStaffAssign.objects.filter(staff=staff).values_list("id")
        assigned_works = OrderWorkStaffTaken.objects.filter(
            id__in=works, taken_date_time__isnull=True
        ).count()
        print(assigned_works)
        return Response(assigned_works)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# STAFF ON GOING WORKS
@api_view(["POST"])
def staff_taken_works(request):
    data = request.data
    if data["login_id"]:
        login_id = data["login_id"]
        staff = fetchStaff(login_id)
        works = OrderWorkStaffAssign.objects.filter(staff=staff).values_list("id")
        taken_works = OrderWorkStaffTaken.objects.filter(
            id__in=works, taken_date_time__isnull=False
        ).count()
        return Response(taken_works)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# STAFF TODAY DUE WORKS
@api_view(["POST"])
def staff_today_due_works(request):
    data = request.data
    if data["login_id"]:
        login_id = data["login_id"]
        staff = fetchStaff(login_id)
        today_due_orders = Order.objects.filter(
            due_date=datetime.date.today()
        ).values_list("order_id")
        order_work_id = OrderWorkStaffAssign.objects.filter(
            staff=staff, order_id__in=today_due_orders
        ).values_list("id")
        taken_works = OrderWorkStaffTaken.objects.filter(
            orderworkstaffassign_id__in=order_work_id
        ).count()
        return Response(taken_works)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# STAFF WEEK DUE WORKS
@api_view(["POST"])
def staff_week_due_works(request):
    data = request.data
    if data["login_id"]:
        login_id = data["login_id"]
        staff = fetchStaff(login_id)
        from_date = datetime.date.today() - relativedelta(days=7)
        to_date = datetime.date.today()
        today_due_orders = Order.objects.filter(
            due_date__range=[from_date, to_date]
        ).values_list("order_id")
        order_work_id = OrderWorkStaffAssign.objects.filter(
            staff=staff, order_id__in=today_due_orders
        ).values_list("id")
        taken_works = OrderWorkStaffTaken.objects.filter(
            orderworkstaffassign_id__in=order_work_id, taken_date_time__isnull=False
        ).count()
        return Response(taken_works)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# SUPERVISOR UNASSINGED WORKS
@api_view(["GET"])
def unassigned_works(request):
    unassigned_works = OrderWorkStaffAssign.objects.filter(staff__isnull=True).count()
    return Response(unassigned_works)


# SUPERVISOR NOT TAKEN
@api_view(["GET"])
def not_taken_works(request):
    not_taken_works = OrderWorkStaffTaken.objects.filter(
        taken_date_time__isnull=True
    ).count()
    return Response(not_taken_works)


# SUPERVISOR TODAY COURIER ORDERS
@api_view(["GET"])
def today_due_delivery(request):
    today_due_orders = Order.objects.filter(due_date=datetime.date.today()).values_list(
        "order_id"
    )
    today_delivery = Delivery.objects.filter(order_id__in=today_due_orders).count()
    return Response(today_delivery)


# SUPERVISOR TODAY COURIER ORDERS
@api_view(["GET"])
def week_due_delivery(request):
    from_date = datetime.date.today() - relativedelta(days=7)
    to_date = datetime.date.today()
    today_due_orders = Order.objects.filter(
        due_date__range=[from_date, to_date]
    ).values_list("order_id")
    today_delivery = Delivery.objects.filter(order_id__in=today_due_orders).count()
    return Response(today_delivery)
