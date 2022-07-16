from ast import Mod
from dataclasses import field
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from api.models import *


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        exclude = ("password",)

class WorkSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"


class TmpWorkSerializer(ModelSerializer):
    class Meta:
        model = TmpWork
        fields = "__all__"


class TmpMaterialSerializer(ModelSerializer):
    class Meta:
        model = TmpMaterial
        fields = "__all__"


class MaterialSerializer(ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"


class OrderSerializers(ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Order
        fields = "__all__"


class StaffSerializers(ModelSerializer):
    takenOrders = SerializerMethodField("gettakenOrders")
    assignOrders = SerializerMethodField("getassignOrders")
    nottakenOrders = SerializerMethodField("getnottakenOrders")
    password = SerializerMethodField('getpassword')
    
    def getassignOrders(self,obj):
        orderworkstaffassign = OrderWorkStaffAssign.objects.filter(staff = obj).exclude(assign_stage = 'complete_final_stage')
        # for order in orderworkstaffassign:
        #     order_id = order.order_id
        #     label = order.order_work_label
        #     print(label)
        #     count = OrderWorkStaffAssign.objects.filter(order_work_label=label).exclude(assign_stage = 'complete_final_stage').values_list('assign_stage')
        #     print(count)
            
        c = len(orderworkstaffassign)
        total = 0
        for i in range(0,c):
            check = OrderWorkStaffStatusCompletion.objects.filter(orderworkstaffassign = i,work_staff_completion_approved = True)
            if check:
                total += 0
            else:
                total += 1
        return total

    def gettakenOrders(self, obj):
        orderworkstaffassign = OrderWorkStaffAssign.objects.filter(staff = obj).exclude(assign_stage = 'complete_final_stage').values_list('id')
        taken_work = OrderWorkStaffTaken.objects.filter(id__in = orderworkstaffassign,taken_date_time__isnull = False).values_list('orderworkstaffassign')
        c = OrderWorkStaffTaken.objects.filter(id__in = orderworkstaffassign,taken_date_time__isnull = False).count()
        total = 0
        if c != 0:
            for i in range(0,c):
                check = OrderWorkStaffStatusCompletion.objects.filter(orderworkstaffassign_id = taken_work[i],work_staff_completion_approved = True)
                if check:
                    total += 0
                else:
                    total += 1
            return total
            
        else:
            return total
    
    def getnottakenOrders(self, obj):
        orderworkstaffassign = OrderWorkStaffAssign.objects.filter(staff = obj).exclude(assign_stage = 'complete_final_stage').values_list('id')
        taken_work = OrderWorkStaffTaken.objects.filter(id__in = orderworkstaffassign,taken_date_time__isnull = True).values_list('orderworkstaffassign')
        c = OrderWorkStaffTaken.objects.filter(id__in = orderworkstaffassign,taken_date_time__isnull = True).count()
        total = 0
        if c != 0:
            for i in range(0,c):
                print(taken_work[i])
                check = OrderWorkStaffStatusCompletion.objects.filter(orderworkstaffassign_id = taken_work[i],work_staff_completion_approved = True)
                if check:
                    total += 0
                else:
                    total += 1
            return total
            
        else:
            return total

    def getpassword(self,obj):
        password = User.objects.get(login_id = obj.staff_id)
        return password.password

    class Meta:
        model = Staff
        fields = "__all__"


class OrderWorkStaffAssignSerializers(ModelSerializer):
    order = OrderSerializers()
    work = WorkSerializer()
    staff = StaffSerializers()

    class Meta:
        model = OrderWorkStaffAssign
        fields = "__all__"


class OrderWorkStaffTakenSerializers(ModelSerializer):
    orderworkstaffassign = OrderWorkStaffAssignSerializers()

    class Meta:
        model = OrderWorkStaffTaken
        fields = "__all__"


class OrderWorkStaffAssignCompletionSerializers(ModelSerializer):
    order = OrderSerializers()
    staff = StaffSerializers()
    orderworkstaffassign = OrderWorkStaffAssignSerializers()

    class Meta:
        model = OrderWorkStaffStatusCompletion
        fields = "__all__"


class OrderStatusSerializers(ModelSerializer):
    order = OrderSerializers()
    staff = StaffSerializers()
    orderworkstaffassign = OrderWorkStaffAssignSerializers()

    class Meta:
        model = OrderWorkStaffStatusCompletion
        fields = "__all__"


class StaffWorkWageSerializers(ModelSerializer):
    class Meta:
        model = StaffWorkWage
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"


class OrderSerializer(ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Order
        fields = "__all__"


class OrderWorkStaffAssignSerializer(ModelSerializer):
    order = OrderSerializer()
    work = WorkSerializer()
    staff = StaffSerializer()

    class Meta:
        model = OrderWorkStaffAssign
        fields = "__all__"


class OrderWorkSerializer(ModelSerializer):
    order = SerializerMethodField("getOrder")
    work = SerializerMethodField("getWork")
    customer = SerializerMethodField("getCustomer")

    def getOrder(self,obj):
        order = Order.objects.get(order_id = obj.order_id)
        serializer = OrderSerializer(order)
        return serializer.data

    def getWork(self,obj):
        work = Work.objects.get(work_id = obj.work_id)
        serializer = WorkSerializer(work)
        return serializer.data

    def getCustomer(self,obj):
        order = Order.objects.get(order_id = obj.order_id)
        customer = Customer.objects.get(cust_id = order.customer.cust_id)
        serializer = CustomerSerializer(customer)
        return serializer.data
      
    class Meta:
        model = OrderWork
        fields = "__all__"

class OrderMaterialSerializer(ModelSerializer):
    class Meta:
        model = OrderMaterial
        fields = "__all__"


class OrderMaterialLocationSerializer(ModelSerializer):
    class Meta:
        model = OrderMaterialLocation
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class DeliverySerializer(ModelSerializer):
    orderwork = OrderWorkSerializer()
    staff = StaffSerializer()

    class Meta:
        model = Delivery
        fields = "__all__"

class OrderWorkStaffStatusCompletionSerializer(ModelSerializer):
    order = OrderSerializer()
    staff = StaffSerializer()
    orderworkstaffassign = OrderWorkStaffAssignSerializer()
    class Meta:
        model = OrderWorkStaffStatusCompletion
        fields = "__all__"


class CustomerListSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class OrderAssignAdminSerializers(ModelSerializer):
    staff = StaffSerializers()
    ordertaken = SerializerMethodField('orderTaken')
    ordercompletion = SerializerMethodField('orderCompletion')
    materiallocation = SerializerMethodField('getMaterialLocation')

    def getMaterialLocation(self,obj):
        location = OrderMaterialLocation.objects.filter(order_work_label = obj.order_work_label,staff=obj.staff).last()
        serializer = OrderMaterialLocationSerializer(location)
        if location:
            return serializer.data
        else:
            data = {
                "materaillocation": None
            }
            return data

    def orderTaken(self,obj):
        orderTaken = OrderWorkStaffTaken.objects.filter(orderworkstaffassign = obj).values('taken_date_time')

        if orderTaken:
            return orderTaken[0]
        else:
            data = {
                "taken_date_time": None
            }
            return data

    def orderCompletion(self,obj):
        orderComplete = OrderWorkStaffStatusCompletion.objects.filter(orderworkstaffassign = obj).values('work_completed_date_time')
        if orderComplete:
            return orderComplete[0]
        else:
            data = {
                "work_completed_date_time": None
            }
            return data


    class Meta:
        model = OrderWorkStaffAssign
        fields = "__all__"


class EligibleDeliverySerializer(ModelSerializer):
    order = OrderSerializers()
    staff = StaffSerializers()

    class Meta:
        fields = '__all__'
        model = EligibleDelivery

class TmpDeliverySerializer(ModelSerializer):
    order = OrderSerializers()
    staff = StaffSerializers()
    class Meta:
        fields = '__all__'
        model = TmpDelivery

class CustomerMeasurementSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = CustomerMeasurement

class FamilyMemberSerializer(ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        fields = '__all__'
        model = FamilyMember

class UrgentOrderSerializer(ModelSerializer):
    customer = CustomerSerializer()
    order = OrderSerializers()
    staff = StaffSerializers()
    class Meta:
        fields = '__all__'
        model = UrgentOrder
