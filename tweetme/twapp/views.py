from http.client import HTTPResponse
import random
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse,HttpResponseRedirect

from tweetme.settings import ALLOWED_HOSTS
from .models import Tweet
from .forms import TweetForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import  settings



# ALLOWED_HOSTS = settings.ALLOWED_HOSTS 
# Create your views here.
def home_view(request,*args,**kwargs):
    #print(args,kwargs)
    # return HttpResponse("hello world")
    return render(request,"pages/home.html",context={},status=200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url= request.POST.get("next") or None
    print('post data is ', request.POST)
    if form.is_valid():
        obj=form.save(commit=False)
        obj.save()
        if next_url !=None and url_has_allowed_host_and_scheme(next_url,ALLOWED_HOSTS) :
            return redirect(next_url)
        form = TweetForm()
    return render(request ,'components/form.html',context={"form":form})

def tweet_list_view(request,*args,**kwargs):
    qs=Tweet.objects.all()
    tweet_list= [{"id": x.id,  "content":x.content , "likes": random.randint(0,232)} for x in qs]
    data= {
        "isUser": False,
        "response": tweet_list
    }
    return JsonResponse(data)

def tweet_detail_view(request,tweet_id,*args,**kwargs):

    """
    REST API VIEW 
      return json data
    """
    
    #print(args,kwargs,tweet_id)
    data={
        "id":tweet_id,
        # "content":obj.content,
    }
    status=200
    try:
        obj=Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
   
    return JsonResponse(data,status=status)
    # return HttpResponse(f"hello  {tweet_id}- {obj.content}")