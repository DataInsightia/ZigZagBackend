import json
from rest_framework.response import Response
from api.models import *

def get_ifsc(ifsc):
    try:
        with open('./ifsc.json', 'r') as f:
            search_ifsc = json.load(f)

            
            for check_ifsc in search_ifsc:
                if check_ifsc['IFSC'] == ifsc:
                    return check_ifsc
                else:
                    data = {
                        "IFSC":"","BANK":""
                    }
                    return data
    except Exception as e:
        return Response({'status' : False, 'error' : str(e)})


def fetchStaff(staff_id):
    try:
        return Staff.objects.get(staff_id = staff_id)
    except Staff.DoesNotExist:
        resp = NotfoundContext('staff id not found')
        return Response(resp,status=status.HTTP_404_NOT_FOUND)

def fetchWork(work_id):
    try:
        return Work.objects.get(work_id = work_id)
    except Work.DoesNotExist:
        resp = NotfoundContext('work id not found')
        return Response(resp,status=status.HTTP_404_NOT_FOUND)

def fetchOrder(order_id):
    try:
        return Order.objects.get(order_id = order_id)
    except Order.DoesNotExist:
        resp = NotfoundContext('order id not found')
        return Response(resp,status=status.HTTP_404_NOT_FOUND)

def getNextStage(order_id):
    order = fetchOrder(order_id)
    s =  OrderWorkStaffAssign.objects.filter(order = order)
    exclude_list = ['cutting','stitching','hook','overlock']
    for i in s:
        if i.assign_stage in exclude_list: 
            exclude_list.remove(i.assign_stage)
        else:
            pass
    if exclude_list != [] :
        return exclude_list[0]
    else:
        return "Completed"

def SuccessContext(status,message,details):
    data = {
        "status":status,
        "message":message,
        "details":details
    }
    return data

def ErrorContext(status,message,details):
    data = {
        "status":status,
        "message":message,
        "details":details
    }
    return data

def KeyErrorContext(status,message,error):
    data = {
        "status":status,
        "message":message,
        "error":error
    }
    return data

def NotfoundContext(error):
    data = {
        "Error":error,
    }
    return data