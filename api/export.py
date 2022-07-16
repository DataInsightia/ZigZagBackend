import xlwt
from django.http import HttpResponse
from api.models import *
from rest_framework.decorators import api_view

@api_view(["GET"])
def export_excel(request,table_name):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    if "customers" == table_name:
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(table_name)
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['CUSTOMER ID','CUSTOMER NAME','MOBILE','EMAIL','ADDRESS','CITY','PINCODE','COUNTRY CODE']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = Customer.objects.all().values_list('cust_id','cust_name','mobile','email','address','city','pincode','country_code')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    elif "staffs" == table_name:
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(table_name)
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['STAFF ID','STAFF NAME','MOBILE','ADDRESS','CITY','SALARY TYPE','SALARY','ACCOUNT NO','BANK','IFSC','WORK TYPE']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = Staff.objects.all().values_list('staff_id','staff_name','mobile','address','city','salary_type','salary','acc_no','bank','ifsc','work_type')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    elif "products" == table_name:
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(table_name)
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['PRODUCT ID','PRODUCT NAME','NEW ARRIVAL','DISPLAY','CREATED AT']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = Product.objects.all().values_list('product_id','product_name','new_arrival','display','created_at')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    elif "works" == table_name:
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(table_name)
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['WORK ID','WORK NAME','WAGE TYPE','AMOUNT']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = Work.objects.all().values_list('work_id','work_name','wage_type','amount')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    elif "materials" == table_name:
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(table_name)
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['MATERIAL ID','MATERIAL NAME','MEASUREMENT','AMOUNT']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = Material.objects.all().values_list('material_id','material_name','measurement','amount')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response