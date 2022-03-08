from django.urls import path
from . import views

urlpatterns = [
    path("test/", views.test),
    path("customer_register/", views.customer_register),
    path("customer_login/", views.customer_login),
    path("customer_details/", views.customer_details),
    path("works/", views.works),
    path("orders/", views.orders),
    path("materials/", views.materials),
    path("generate_orderid/", views.generate_orderid),
    path("tmp_work/", views.tmp_work),
    path("tmp_material/", views.tmp_material),
    path("tmp_works/", views.tmp_works),
    path("tmp_materials/", views.tmp_materials),
    path("del_tmpwork/", views.del_tmpwork),
    path("del_tmpmaterial/", views.del_tmpmaterial),
    path("get_tmpwork/", views.get_tmpwork),
    path("get_tmpmaterial/", views.get_tmpmaterial),
    path("add_order/", views.add_order),
    path("add_order_work/", views.add_order_work),
    path("add_order_material/", views.add_order_material),
    path("staff_register/", views.staff_register),
    path("staff_login/", views.staff_login),
    path("order_status/", views.order_status),
    path("order_status_admin/", views.order_status_admin),
    path("staff_work_assign/", views.staff_work_assign),
    path("staff_work_assigned/", views.staff_work_assigned),
    path("staff_work_taken/", views.staff_work_taken),
    path("staff_work_take/", views.staff_work_take),
    path("staff_stage_completion/", views.staff_stage_completion),
    path("staff_work_completion_review/", views.staff_work_completion_review),
    path("staff_work_assign_completion/", views.staff_work_assign_completion),
    path("staff_work_assign_completion_app/", views.staff_work_assign_completion_app),
    path(
        "staff_work_assign_completion_approval/",
        views.staff_work_assign_completion_approval,
    ),
    path("staff/", views.staff),
    path("staff_wage_calculation/", views.staff_wage_calculation),
    path("staff_wage_manager/", views.staff_wage_manager),
    path("order_work_staff_assign/", views.OrderWorkStaffAssignView.as_view()),
    path(
        "order_work_staff_assign/<int:order_id>",
        views.OrderWorkStaffAssignView.as_view(),
    ),
    path("get_details/", views.get_details),
    path("file_upload", views.upload_file),
    path("work_completed/", views.work_completed),
    path("material/", views.MaterialLocationView.as_view()),
    path("get_wagetotal/", views.getWageTotal),
    path("createnew/", views.createnew),
    path("pending_wage/", views.pending_wage),
    path("order_status_oa/", views.order_status_from_order_assign),
    path("order_status_oa_admin/", views.order_status_from_order_assign_admin),
]
