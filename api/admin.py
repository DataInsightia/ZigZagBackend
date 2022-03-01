from csv import list_dialects
from django.contrib import admin
from api.models import *

admin.site.register(
    [
        Material,
        OrderMaterial,
        OrderMaterialLocation,
        StaffWorkWage,
        StaffWageGivenStatus,
        OrderPickupCourier,
        OrderPickupOther,
        OrderPayment,
        Delivery,
        OrderAlter,
        TmpMaterial,
        TmpWork,
    ]
)

@admin.register(OrderWorkStaffAssign)
class OrderWorkStaffAssing(admin.ModelAdmin):
    list_display = ('order','work','staff','assign_stage','assign_date_time')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id','booking_date_time','due_date','total_amount','advance_amount','balance_amount')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cust_id','password','cust_name','mobile','email','address','city','pincode')

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('work_id','work_name','wage_type','amount')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id','staff_name','mobile','address','salary_type','salary','acc_no','bank','ifsc','work_type')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('login_id','password','mobile','role')

@admin.register(OrderWorkStaffTaken)
class OrderWorkStaffTakenAdmin(admin.ModelAdmin):
    list_display = ('orderworkstaffassign','taken_date_time')

@admin.register(OrderWorkStaffStatusCompletion)
class OrderWorkStaffStatusCompletionAdmin(admin.ModelAdmin):
    list_display = ('id','order','staff','orderworkstaffassign','work_completed_date_time','work_staff_comp_app_date_time','work_staff_completion_approved','order_next_stage_assign')
