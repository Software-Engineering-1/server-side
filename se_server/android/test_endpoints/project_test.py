import requests
URL="http://127.0.0.1:8000/android/add_project"


r=requests.post(URL,data={'user_name':'kai123456android','password':'kai123456android',
'name':'P1','duration':6,'url':'www.google.com','description':'Project'})
print(r.text,r.status_code)