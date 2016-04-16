import requests
URL="http://127.0.0.1:8000/android/add_person_organization"


r=requests.post(URL,data={'user_name':'kai123456android','password':'kai123456android',
'startDate':'1996-01-01','endDate':'1997-02-02','organization':'KAImax','title':'Manager'})
print(r.text,r.status_code)