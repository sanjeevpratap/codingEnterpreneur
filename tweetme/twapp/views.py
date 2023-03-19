from http.client import HTTPResponse
import random
from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponse,Http404,JsonResponse,HttpResponseRedirect

from tweetme.settings import ALLOWED_HOSTS
from .models import Tweet
from .forms import TweetForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import  settings
from .serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializers import TweetSerializer,TweetActionSerializer,TweetCreateSerializer


def home_view(request,*args,**kwargs):
    print(request.user or none)
    #print(args,kwargs)
    # return HttpResponse("hello world")
    return render(request,"pages/home.html",context={},status=200)

@api_view(['POST'])    #http method the client == POST

@permission_classes([IsAuthenticated])     #this deal with permission that user is allowed to do below operations
def tweet_create_view(request, *args, **kwargs):
    serializer= TweetCreateSerializer(data=request.POST )
    if serializer.is_valid(raise_exception=True):
       
        serializer.save(user=request.user )
        return Response(serializer.data,status=201)
    return Response({},status=400)


@api_view(['GET'])   #http method the client == GET
def tweet_detail_view(request,tweet_id,*args,**kwargs):
     qs=Tweet.objects.filter(id=tweet_id)
     if not qs.exists():
        return Response({},status=404)
     obj =qs.first()
     serializer= TweetSerializer(obj)
    
     return Response(serializer.data,status=200)

     
@api_view(['DELETE','POST'])   #http method the client == GET
@permission_classes([IsAuthenticated])
def tweet_delete_view(request,tweet_id,*args,**kwargs):
     qs=Tweet.objects.filter(id=tweet_id)
     if not qs.exists():
        return Response({},status=404)
     qs=qs.filter(user=request.user)
     if not qs.exists():
        return Response({"message": " you cannot delete this tweet"},status=401  )
     obj =qs.first()
     obj.delete()
     #serializer= TweetSerializer(obj)
    
     return Response({"message":"Tweet deleted"},status=200)


@api_view(['POST'])   #http method the client == GET
@permission_classes([IsAuthenticated])
def tweet_action_view(request,*args,**kwargs):

    '''
    id is required.
    Action options are: like,unlike,retweet
    '''
    print(request.POST,request.data)
    serializer =TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
       data = serializer.validated_data
       tweet_id =data.get("id")
       action =data.get("action")
       content=data.get("content")
       print(data)
       qs=Tweet.objects.filter(id=tweet_id)
       if not qs.exists():
          return Response({},status=404)
       
       obj =qs.first()
       if action == "like":
          obj.likes.add(request.user)
          serializer =TweetSerializer(obj)
          return Response(serializer.data,status=200)

       elif action == "unlike":
          obj.likes.remove(request.user)
          serializer =TweetSerializer(obj)
          return Response(serializer.data,status=200)
       elif action == "retweet":

        
        new_tweet = Tweet.objects.create(user=request.user,parent=obj,content=content,) #creating retweet parent
        serializer =TweetSerializer(new_tweet)
        return Response(serializer.data,status=201)
        

    

    return Response({},status=200)

@api_view(['GET'])   #http method the client == GET
def tweet_list_view(request,*args,**kwargs):
     qs=Tweet.objects.all()
     serializer= TweetSerializer(qs,many=True)
    
     return Response(serializer.data)







def tweet_create_view_pure_django(request, *args, **kwargs):
    # print(abc)   for server error checking
    user =request.user
    if not request.user.is_authenticated:
        user= None
        if request.accepts("pages/home.html"):
            
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url= request.POST.get("next") or None
   
    
    if form.is_valid():
        print("valid")
        
        obj=form.save(commit=False)
        obj.user =request.user or None     #Annamous user(none user)
        obj.save()
        
        if request.accepts("pages/home.html"):
            return JsonResponse(obj.serialize(), status=201)    # 201 == created items
        # if next_url !=None and is_safe_url(next_url,ALLOWED_HOSTS) :
        if next_url !=None and url_has_allowed_host_and_scheme(next_url,ALLOWED_HOSTS) :
            
            return redirect(next_url)
        
        form = TweetForm()
    if form.errors:
        if request.accepts("pages/home.html"):
            
            return JsonResponse(form.errors, status=400)
    
    return render(request ,'components/form.html',context={"form":form})



def tweet_list_view_pure_django(request,*args,**kwargs):
    qs=Tweet.objects.all()
    tweet_list= [ x.serialize() for x in qs]
    # tweet_list= [{"id": x.id,  "content":x.content , "likes": random.randint(0,232)} for x in qs]
    data= {
        "isUser": False,
        "response": tweet_list
    }
    return JsonResponse(data)

def tweet_detail_view_pure_django(request,tweet_id,*args,**kwargs):

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