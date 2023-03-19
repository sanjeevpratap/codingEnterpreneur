from django.db import models
import random
from django.conf import settings
from django.db import models


User =settings.AUTH_USER_MODEL
# Create your models here.

class TweetLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet",on_delete=models.CASCADE)
    timestamp =models.DateTimeField(auto_now_add=True)
class Tweet(models.Model):
    # Map to SQL DATA
    #id = models.AutoFields(primary_key=True)
    parent = models.ForeignKey("self",null=True,on_delete=models.SET_NULL)
    user =models.ForeignKey(User , on_delete=models.CASCADE)    # one users can have many tweets
    likes =models.ManyToManyField(User,related_name='tweet_user',blank=True,through=TweetLike)
    content=models.TextField(blank=True, null=True)
    image= models.FileField(upload_to='images/', blank=True, null=True)
    timestamp =models.DateTimeField(auto_now_add=True)
    
   
    class Meta:
        ordering = ['-id']

    @property
    def is_retweet(self):
        return self.parent !=None
    
    # def serialize(self):    created when serializer file was not there and changig in to json in model not in view.
    #     return {
    #         "id": self.id,
    #         "content": self.content,
    #         "likes": random.randint(0,200)
    #     }