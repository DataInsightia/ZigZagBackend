import json
from rest_framework.response import Response
from api.models import *
from rest_framework import status

def get_ifsc(ifsc):
    try:
        with open("./ifsc.json", "r") as f:
            search_ifsc = json.load(f)

            for check_ifsc in search_ifsc:
                if check_ifsc["IFSC"] == ifsc:
                    return check_ifsc
                else:
                    data = {"IFSC": "", "BANK": ""}
                    return data
    except Exception as e:
        return Response({"status": False, "error": str(e)})


def fetchStaff(staff_id):
    try:
        return Staff.objects.get(staff_id=staff_id)
    except Staff.DoesNotExist:
        resp = NotfoundContext("staff id not found")
        return Response(resp, status=status.HTTP_404_NOT_FOUND)


def fetchWork(work_id):
    try:
        return Work.objects.get(work_id=work_id)
    except Work.DoesNotExist:
        resp = NotfoundContext("work id not found")
        return Response(resp, status=status.HTTP_404_NOT_FOUND)


def fetchOrder(order_id):
    try:
        return Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        resp = NotfoundContext("order id not found")
        return Response(resp, status=status.HTTP_404_NOT_FOUND)


def getNextStage(order_id, order_work_label):
    order = fetchOrder(order_id)
    s = OrderWorkStaffAssign.objects.filter(
        order=order, order_work_label=order_work_label
    )
    exclude_list = ["cutting", "stitching", "hook", "overlock", "Completed"]
    for i in s:
        if i.assign_stage in exclude_list:
            exclude_list.remove(i.assign_stage)
        else:
            pass
    include_list = ["cutting", "stitching", "hook", "overlock", "Completed"]
    finish_list = []
    for i in s:
        if i.assign_stage in include_list:
            finish_list.append(i.assign_stage)
        else:
            pass

    k = ["stage"]
    n = len(finish_list)
    include_res = []
    if finish_list != []:
        for idx in range(0, n, 1):
            include_res.append({k[0]: finish_list[idx]})

    k = ["stage"]
    n = len(exclude_list)
    exclude_res = []
    if exclude_list != []:
        for idx in range(0, n, 1):
            exclude_res.append({k[0]: exclude_list[idx]})

    if exclude_list != []:
        data = {"nextassign": exclude_res, "finishedassign": include_res}
        return data
    else:
        data = {"nextassign": exclude_res, "finishedassign": include_res}
        return data


def SuccessContext(status, message, details):
    data = {"status": status, "message": message, "details": details}
    return data


def ErrorContext(status, message, details):
    data = {"status": status, "message": message, "details": details}
    return data


def KeyErrorContext(status, message, error):
    data = {"status": status, "message": message, "error": error}
    return data


def NotfoundContext(error):
    data = {
        "Error": error,
    }
    return data


def generate_ID(code,db):
    try:
        start_order_number = 786

        if db.objects.all().last() != None:
            if Material == db:
                order = db.objects.all().last()
                last_order_id = order.material_id
                start_order_number = 786
                if int(last_order_id[2:]) % 1000 == 0:
                    next_letter = chr(ord(last_order_id[1]) + 1)
                    o_id = "Z" + next_letter + str(start_order_number)
                    return o_id
                else:
                    next_letter = chr(ord(last_order_id[1]) + 0)
                    o_id = "Z" + next_letter + str(int(last_order_id[2:]) + 1)
                    return o_id
            else:
                order = db.objects.all().last()
                last_order_id = order.work_id
                start_order_number = 786
                if int(last_order_id[2:]) % 1000 == 0:
                    next_letter = chr(ord(last_order_id[1]) + 1)
                    o_id = "Z" + next_letter + str(start_order_number)
                    return o_id
                else:
                    next_letter = chr(ord(last_order_id[1]) + 0)
                    o_id = "Z" + next_letter + str(int(last_order_id[2:]) + 1)
                    return o_id
        else:
            o_id = code + str(start_order_number)
            return o_id
    except Exception as e:
        return Response({"status": True, "error": str(e)})

def fetchCustomer(login_id):
    try:
        return Customer.objects.get(cust_id=login_id)
    except Customer.DoesNotExist:
        resp = NotfoundContext("customer id not found")
        return Response(resp, status=status.HTTP_404_NOT_FOUND)

