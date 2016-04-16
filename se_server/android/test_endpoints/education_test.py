import requests
URL="http://127.0.0.1:8000/android/add_education"


r=requests.post(URL,data={'user_name':'kai123456android','password':'kai123456android',
'name':'SVM','grad_year':'2014','degree':'B','field_of_study':'','score':'100'})
print(r.text,r.status_code)