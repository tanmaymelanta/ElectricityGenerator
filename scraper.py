import requests
import pandas as pd

url = "https://webapi.grid-india.in/api/v1/file"

payload = {
    "_source": "GRDW",
    "_type": "DAILY_PSP_REPORT",
    "_fileDate": "2013-14",
    "_month": "00"
}

response = requests.post(url, json=payload)

response.raise_for_status()

data = response.json()["retData"]

df = pd.DataFrame(data)

print(df.head())

df.to_csv("daily_psp_2013_14.csv", index=False)
