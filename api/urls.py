from django.urls import path, re_path
from . import views
from api.export import *

urlpatterns = [
    path("test/", views.test),
    path("customer_register/", views.customer_register),
    path("customer_login/", views.customer_login),
    path("customer_details/", views.customer_details),
    path("takeorder_customer_details/", views.takeorder_customer_details),
    path("is_user/", views.is_user),
    path("is_staff/", views.is_staff),
    path("works/", views.works.as_view()),
    # path("works/<work_id>", views.works.as_view()),
    re_path(r"works/(?P<work_id>[Z|z][W|w][0-9]{2,8})/$", views.works.as_view()),
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
    # path('staff_login/',views.staff_login),
    path("order_status/", views.order_status),
    path("staff_work_assign/", views.staff_work_assign),
    path("staff_work_assign_by_order/", views.staff_work_assign_by_order),
    path("staff_work_assigned/", views.staff_work_assigned),
    path("staff_work_taken/", views.staff_work_taken),
    path("staff_stage_completion/", views.staff_stage_completion),
    path("staff_work_completion_review/", views.staff_work_completion_review),
    path("staff_work_assign_completion/", views.staff_work_assign_completion),
    path("staff_work_assign_completion_app/", views.staff_work_assign_completion_app),
    # path('staff_work_assign_completion_approval/',views.staff_work_assign_completion_approval),
    path("staff/", views.staff),
    path("staff_wage_calculation/", views.staff_wage_calculation),
    # path('staff_wage_manager/',views.staff_wage_manager),
    path("order_work_staff_assign/", views.OrderWorkStaffAssignView.as_view()),
    # path(
    #     "order_work_staff_assign/<int:order_id>",
    #     views.OrderWorkStaffAssignView.as_view(),
    # ),

    re_path(
        r"order_work_staff_assign/(?P<orderid>[Z|z][a-z|A-Z][7-9][0-9]{2,})/$",
        views.OrderWorkStaffAssignView.as_view(),
    ),
    path("get_details/", views.get_details),
    path("file_upload", views.upload_file),
    path("work_completed/", views.work_completed),
    path("materialc/", views.MaterialLocationView.as_view()),
    # path("material/<orderid>/", views.MaterialLocationView.as_view()),
    re_path(r'material/(?P<orderid>[Z|z][a-z|A-Z][7-9][0-9]{2,8})/$', views.MaterialLocationView.as_view()),

    # path("get_wagetotal/", views.getWageTotal),
    # path("createnew/", views.createnew),
    path("pending_wage/", views.pending_wage),
    path("order_status_oa/", views.order_status_from_order_assign),
    path("order_status_oa_admin/", views.order_status_from_order_assign_admin),
    path("order_status_from_oa_admin",views.order_status_from_oa_admin),
    path("order_admin_status/", views.order_admin_status),
    path("order_status_admin_v2/",views.order_status_admin_v2),
    path("order_status_oa_admin",views.order_status_oa_admin),
    path("admin_orders/", views.AdminOrder.as_view()),
    path("work_completed/", views.work_completed),
    # path("customer_orders/<custid>/", views.CustomerOrder.as_view()),
    re_path("customer_orders/(?P<custid>[Z|z]C[0-9]{2,8})/$", views.CustomerOrder.as_view()),
    path("order_invoice/", views.OrderInvoiceView.as_view()),
    path("staff_payment_update/", views.staff_payment_update),
    path("staff_wage_paid_completion/", views.staff_wage_paid_completion),
    path("staff_wage_status/<str:status>", views.staff_wage_status),
    path("product/", views.ProductView.as_view()),
    path("product/<productid>/", views.ProductView.as_view()),
    path("get_product/", views.get_product),
    path("product_display/", views.product_to_display),
    path("new_arrivals/", views.new_arrivals),
    path("products/", views.get_products),
    # path('staff_wage_paid/',views.staff_wage_paid),
    path("pending_wage/", views.pending_wage),
    path("staff_payment_update/", views.staff_payment_update),
    path("staff_wage_paid_completion/", views.staff_wage_paid_completion),
    path("staff_wage_status/<str:status>", views.staff_wage_status),
    # path("customer_orders/<custid>/", views.CustomerOrder.as_view()),
    re_path("customer_orders/(?P<custid>[Z|z]C[0-9]{2,8})/$", views.CustomerOrder.as_view()),
    path("order_invoice/", views.OrderInvoiceView.as_view()),
    path("material/", views.MaterialLocationView.as_view()),
    path("order_status_oa/", views.order_status_from_order_assign),
    path("order_status_oa_admin/", views.order_status_from_order_assign_admin),
    path("admin_orders/", views.AdminOrder.as_view()),
    # path("customer_orders/<orderid>/<custid>/", views.CustomerOrder.as_view()),
    re_path(r'customer_orders/(?P<orderid>[Z|z][a-z|A-Z][7-9][0-9]{2,8})/(?P<custid>[Z|z]C[0-9]{2,8})/$', views.CustomerOrder.as_view()),

    path("customers/", views.customers),
    path("mat/", views.MaterialView.as_view()),
    #
    # path("mat/<mat_id>", views.MaterialView.as_view()),
    re_path(r"mat/(?P<mat_id>[Z|z][M|m][0-9]{2,8})/$", views.MaterialView.as_view()),
    # customer order counts
    path('customer_total_orders/',views.customer_total_orders),
    path('customer_pending_orders/',views.customer_pending_orders),
    path('customer_completed_orders/',views.customer_completed_orders),
    path('customer_delivery_ready/',views.customer_delivery_ready),

    #staff order counts
    path('staff_total_works/',views.staff_total_works),
    path('staff_not_taken_works/',views.staff_not_taken_works),
    path('staff_taken_works/',views.staff_taken_works),
    path('staff_today_due_works/',views.staff_today_due_works),
    path('staff_week_due_works/',views.staff_week_due_works),


    #SUPERVISOR
    path('unassigned_works/',views.unassigned_works),
    path('not_taken_works/',views.not_taken_works),
    path('today_due_works/',views.today_due_delivery),
    path('week_due_works/',views.week_due_delivery),

    #WORK DETAIL
    # path('work/<work_id>/',views.workdetail),
    re_path(r'work/(?P<work_id>[Z|z][W|w][7-9][0-9]{2,8})/$',views.workdetail),

    # DELIVERY
    path("is_order_completed/",views.is_order_completed),
    path("order_assign_completed/",views.order_assign_completed),
    path("fix_delivery_true/",views.fix_delivery_true),
    
    # path('mate/<mate_id>/',views.mateid),
    re_path(r'mate/(?P<mate_id>[Z|z][M|m][0-9]{2,8})/$',views.mateid),

    # ORDER COMPLETION
    path("order_completion/",views.order_completion),

    # TAKE ORDER OTHER
    path("takeorder_other_option/",views.takeorder_other_option),
    path("proceed_other_delivery/",views.proceed_other_delivery),

    # PAY ADVANCE
    path("proceed_pay_advance/",views.proceed_pay_advance),

    # GET SPECIFIC ORDER
    # path("find_order/<orderid>",views.OrderView.as_view()),
    re_path(r'find_order/(?P<orderid>[Z|z][a-z|A-Z][7-9][0-9]{2,8})/$',views.OrderView.as_view()),

    path('order_status_admin/',views.order_status_admin),
    path("is_order/",views.is_order),

    path('display_dashboard/<state>/',views.display_dashboard),
    path("tmp_delivery/", views.tmp_delivery),

    path("customer_measurement/", views.CustomerMeasurementView.as_view()),
    path("family_members/",views.FamilyMemberView.as_view()),
    path("get_family_members/",views.get_family_members),

    path("order_filter/",views.order_filter),
    path("mobile_filter/",views.mobile_filter),
    path("order_range_filter/",views.order_range_filter),
    path("order_date_filter/",views.order_date_filter),
    path("loaduserdata/",views.LoaduserData),
    path("user/",views.LoadUserView.as_view()),

    path("delete_delivery/",views.delete_delivery),
    path("add_delivery/",views.add_delivery),
    path("export/<table_name>/", export_excel, name='export_excel'),
    re_path(r'delete_order/(?P<orderid>[Z|z][a-z|A-Z][7-9][0-9]{2,8})/$', views.delete_order),
    path("urgent_order/",views.UrgentOrderView.as_view()),
    path("customer_completed_orders_by_order/",views.customer_completed_orders_by_order),
    path('staff_work_take/',views.staff_work_take),
    path('ordermaterialview/',views.Material_Location_View.as_view()),

    #dropdown
    path('staff_dropdown/',views.StaffDropdown_View.as_view()),
    path('family_dropdown/',views.FamilyMemberDropdown_View.as_view()),
    path('work_dropdown/',views.works_dropdown.as_view()),
    path('material_dropdown/',views.materials_dropdown.as_view()),

    path('add_order_mobile/',views.add_order_mobile.as_view()),    


    # PRINT DELIVERY IN UI_MODULE(DELIVERY)
    path('print_delivery/',views.DeliveryView.as_view()),
    re_path(r'completed_orders/(?P<orderid>[Z|z][a-z|A-Z][7-9][0-9]{2,8})/$', views.completed_order_work_labels),
]
