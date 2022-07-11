from django.urls import path, include
from .views import home, ratings, signup, activate, my_acc, login_view, create_token

urlpatterns = [
    path('', home, name = 'home'),  
    path('signup/', signup, name = 'signup'),  
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        activate, name='activate'),
    path('my-account/', my_acc, name='my-acc'),
    path('login/', login_view, name='login'),
    path('create_token', create_token, name='create_token'),
    path('ratings', ratings, name='ratings')
]
