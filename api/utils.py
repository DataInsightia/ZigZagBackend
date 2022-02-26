import json
from rest_framework.response import Response

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

