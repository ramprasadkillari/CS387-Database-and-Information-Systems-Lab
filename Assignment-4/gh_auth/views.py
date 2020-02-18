from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions, HTTP_HEADER_ENCODING

import requests,json
# Create your views here.

def ghlogin(request):
    # if request.user.is_authenticated:
    return render(request, 'gh_auth.html')

def github_authenticated(request):
    if request.method == 'GET':
        #    auth_code = extract code from request
        # access_token = get_access_token(code) # step 2 in documentation.
        # user_info = get_user_info(access_token) # step 3 in documentation
        code = request.GET.get('code')
        client_id = "bad9e89d458763e238b4"
        client_secret = "3a32cb77801d64a456e2d346b8567df65f86eb33"

        data = {
          
            'client_id':client_id,
            'client_secret':client_secret,
            'redirect_uri':'http://localhost:8000/ghauthenticated/',
            'code':code,

        }
        API_ENDPOINT = "https://github.com/login/oauth/access_token"
        headers = {'Accept': 'application/json'}
        r = requests.post(url = API_ENDPOINT, data = data,headers = headers)

        
        # console.log(r)
        # print(r.headers)
        # headers = json.loads(r.headers)
        # stat = headers['Status'] 
        # print("Status : ",stat)
        if(r.status_code == 200):
            print(r.text)
            tokens = json.loads(r.text)
            if 'error' in tokens:
                return HttpResponse("<html><body>Not Authenticated</body></html>")    
            else:
                access_token = tokens['access_token']
                token_type = tokens['token_type']


                test_api_url = "https://api.github.com/user"
                api_call_headers = {'Authorization': 'Bearer ' + access_token,'Accept': 'application/json' }
                api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)

                user_info =  json.loads(api_call_response.text)
                # print(resp)

                # login = resp['login']
                return HttpResponse("<html><body>"+ str(user_info)+" <body></html>")
            # return HttpResponse("<html><body>" + str(access_token) + " " + str(token_type)+ "</body></html>")
        else:
            return HttpResponse("<html><body>Not Authenticated</body></html>")