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
    nottakenOrders = SerializerMethodField("getnottakenOrders")
    password = SerializerMethodField('getpassword')

    def gettakenOrders(self, obj):
        works = OrderWorkStaffAssign.objects.filter(staff = obj).values_list('id')
        taken_work = OrderWorkStaffTaken.objects.filter(id__in = works,taken_date_time__isnull = False).count()
        return taken_work

    def getnottakenOrders(self, obj):
        works = OrderWorkStaffAssign.objects.filter(staff = obj).values_list('id')
        not_taken_work = OrderWorkStaffTaken.objects.filter(id__in = works,taken_date_time__isnull = True).count()
        return not_taken_work

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


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"


class OrderWorkStaffAssignSerializer(ModelSerializer):
    order = OrderSerializer()
    work = WorkSerializer()
    staff = StaffSerializer()

    class Meta:
        model = OrderWorkStaffAssign
        fields = "__all__"


class OrderWorkSerializer(ModelSerializer):
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
    class Meta:
        model = Delivery
        fields = "__all__"


class CustomerListSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"