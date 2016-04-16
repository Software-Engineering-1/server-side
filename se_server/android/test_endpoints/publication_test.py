import requests
URL="http://127.0.0.1:8000/android/add_publication"


r=requests.post(URL,data={'user_name':'kai123456android','password':'kai123456android',
'conference_name':'CNF','topic':'TPC','field_of_study':'FOS','date_published':'2016-01-01'})
print(r.text,r.status_code)