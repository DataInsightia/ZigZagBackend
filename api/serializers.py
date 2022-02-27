from ast import Mod
from dataclasses import field
from rest_framework.serializers import ModelSerializer
from api.models import *

class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('password',)

class WorkSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'

class TmpWorkSerializer(ModelSerializer):
    class Meta:
        model = TmpWork
        fields = '__all__'

class TmpMaterialSerializer(ModelSerializer):
    class Meta:
        model = TmpMaterial
        fields = '__all__'

class MaterialSerializer(ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class OrderSerializers(ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Order
        fields = "__all__"

class StaffSerializers(ModelSerializer):
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

class OrderStatusSerializers(ModelSerializer):
    order = OrderSerializers()
    staff = StaffSerializers()
    orderworkstaffassign = OrderWorkStaffAssignSerializers()
    class Meta:
        model = OrderWorkStaffStatusCompletion
        fields = "__all__"

class StaffWorkWageSerializers(ModelSerializer):
    order = OrderSerializers()
    staff = StaffSerializers()
    orderworkstatuscompletion = OrderStatusSerializers()
    class Meta:
        model = StaffWorkWage
        fields = "__all__"

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class OrderWorkStaffAssignSerializer(ModelSerializer):
    order = OrderSerializer()
    work = WorkSerializer()
    staff = StaffSerializer()
    class Meta:
        model = OrderWorkStaffAssign
        fields = '__all__'