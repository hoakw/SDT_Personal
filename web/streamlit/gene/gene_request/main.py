from datetime import datetime
import json
import pandas as pd
import time
import datetime

from get_cookie import GetAuthkey

def main():
    ak = GetAuthkey()
    """
    # time 비교 하루 이상 일때 token 값 가져오도록 설계
    time1 = datetime.datetime(2022, 2, 24, 16, 4, 20)
    time2 = datetime.datetime(2022, 2, 25, 16, 4, 20)
    time3 = datetime.datetime(2022, 2, 25, 15, 4, 20)
    time4 = datetime.datetime(2022, 2, 25, 16, 4, 10)

    gap1 = time2 - time1
    gap2 = time3 - time1
    gap3 = time4 - time1
    print(f"gap1 = {gap1.days}, gap2 = {gap2.days}, gap3 = {gap3.days}")
    """
    auth_key, record_time = ak.get_key()

    print(f"Final auth_key = {auth_key}, time = {record_time}")

    """
    h_header = {
        "Cookie": f"authservice_session={auth_key}", 
        "Host": "kfserving-custom-model.user.example.com",
    }

    url_name = "http://192.168.100.184:30890/v1/models/kfserving-custom-model:predict"

    h_data = {
        'gene': 'ASD',
        'sequence': 'FGASTSTASD',
        'case': '1'
    }
    result = requests.post(url_name, headers=h_header, data=json.dumps(h_data)).json()
    print(result)
    #result_df = pd.DataFrame(result)
    """


if __name__ == "__main__":
    main()
#from kfserving import KFServingClient