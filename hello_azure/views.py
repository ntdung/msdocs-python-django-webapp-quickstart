import time

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def index(request, use_s3=False, cache_busting=True, optimizely_s3_bucket='optimizely-staging', account_id='6414039610032128'):
    print('Request for index page received')
    snippet_url = ''
    if use_s3:
        snippet_url = "//%s.s3.amazonaws.com/js/%s.js" % (optimizely_s3_bucket, account_id)
        if cache_busting:
            query_symbol = '&' if '?' in snippet_url else '?'
            snippet_url += query_symbol + 'cache_buster={}'.format(time.time())
    context = {
        'snippet_url': snippet_url,
    }
    return render(request, 'hello_azure/index.html', context)



@csrf_exempt
def hello(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if name is None or name == '':
            print("Request for hello page received with no name or blank name -- redirecting")
            return redirect('index')
        else:
            print("Request for hello page received with name=%s" % name)
            context = {'name': name }
            return render(request, 'hello_azure/hello.html', context)
    else:
        return redirect('index')

@csrf_exempt
def newhello(request):
    if request.method == 'POST':
        name = request.POST.get('newname')

        if name is None or name == '':
            print("Request for hello page received with no name or blank name -- redirecting")
            return redirect('index')
        else:
            print("Request for hello page received with name=%s" % name)
            context = {'name': name}
            return render(request, 'hello_azure/newhello.html', context)
    else:
        return redirect('index')