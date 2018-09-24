import xml.dom.minidom
import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
import os
from sys import platform

'''Debug: The following libraries added to demonstrate Google Oauth 2.0 workflow.'''
from google_auth_oauthlib.flow import Flow
'''Debug: Debug libraries end here.'''



# Create your views here.


def index(request):
    return render(request, 'oauth_views/base.html')


def dashboard(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/fsgim/oauth/')
    else:
        return render(request, 'oauth_views/dashboard.html', {'name': request.user.get_short_name()
                                                              })

def access_api(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/fsgim/api/get')
    else:
        return render(request, 'oauth_views/access_api.html', {'name': request.user.get_short_name()
                                                          })

def get_data_greenbutton(request):
    url = 'https://sandbox.greenbuttonalliance.org:8443/DataCustodian/espi/1_1/resource/Batch/Subscription/1/'
    header = {
        'Authorization': 'Bearer 2a85f4bd-30db-4b7d-8f41-b046b0566cb3',
    }

    r = requests.get(url, headers=header)
    parsedXml = xml.dom.minidom.parseString(r.content)
    pretty_xml_as_string = parsedXml.toprettyxml()
    return render(request, 'oauth_views/access_api.html', {'name': request.user.get_short_name(),
                                                           'get_data': pretty_xml_as_string,
                                                           'get_uri': url
                                                           })

def access_greenbutton_api(request):
    url = 'https://sandbox.greenbuttonalliance.org:8443/DataCustodian/espi/1_1/resource/Batch/Subscription/5/'
    header = {
        'Authorization': 'Bearer 2a85f4bd-30db-4b7d-8f41-b046b0566cb3',
    }

    r = requests.get(url, headers=header)
    parsedXml = xml.dom.minidom.parseString(r.content)
    pretty_xml_as_string = parsedXml.toprettyxml()
    return render(request, 'oauth_views/access_api.html', {'name': request.user.get_short_name(),
                                                           'get_data': pretty_xml_as_string,
                                                           'get_uri': url
                                                           })


def access_google_api(request):

    if platform == "win32" or platform == "cygwin":
        client_secret = os.getcwd() + '\\fsgim_oauth\\client_secrets.json'
    elif platform == "Linux":
        client_secret = os.getcwd() + '/fsgim_oauth/client_secrets.json'

    server = request.get_host()
    redirect_uri = 'http://' + server + '/fsgim/api/'


    flow = Flow.from_client_secrets_file(
        client_secret,
        scopes=['profile', 'email'],
        redirect_uri=redirect_uri)

    # Tell the user to go to the authorization URL.
    auth_url, _ = flow.authorization_url(prompt='consent')
    return HttpResponseRedirect(format(auth_url))
