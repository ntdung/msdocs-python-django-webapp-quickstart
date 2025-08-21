import time

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    print('Request for index page received')
    snippet_url = ''
    # Get use_s3 from request parameters if provided
    use_s3_param = request.GET.get('use_s3')
    if use_s3_param is not None:
        use_s3 = use_s3_param.lower() == 'true'
        if use_s3:
            # Get cache_busting from request parameters if provided
            cache_busting = request.GET.get('cache_busting')
            # Get optimizely_s3_bucket from request parameters if provided
            optimizely_s3_bucket = request.GET.get('optimizely_s3_bucket')
            # Get account_id from request parameters if provided
            account_id = request.GET.get('account_id')
            # , use_s3=True, cache_busting=True, optimizely_s3_bucket='optimizely-staging', account_id='6414039610032128'
            #?use_s3=true&cache_busting=true&optimizely_s3_bucket=optimizely-staging&account_id=6414039610032128
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