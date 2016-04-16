import requests
URL="http://127.0.0.1:8000/android/register"



r=requests.post(URL,data={'user_name':'kai123456','password':'kai123456','email_id':'kai@kai.com'})
print(r.text,r.status_code)


r=requests.post(URL,data={'user_name':'kai123456','password':'kai123456'})
print(r.text,r.status_code)


r=requests.post(URL,data={'user_name':'kai123456android','password':'kai123456android','email_id':'kai@kai.com'})
print(r.text,r.status_code)

