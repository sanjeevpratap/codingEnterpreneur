
from django.urls import path
from twapp.views import (
    tweet_delete_view,
    tweet_action_view
)
from twapp.views import home_view, tweet_detail_view
from twapp.views import tweet_list_view,tweet_create_view
urlpatterns = [
    
    path('', tweet_list_view),
    path('create', tweet_create_view,name="create"),
    path('action',tweet_action_view),
    path('<int:tweet_id>', tweet_detail_view),
    path('<int:tweet_id>/delete', tweet_delete_view),
    

]

