from django.urls import path
from accounts.views import(
            home,
            login_view,
            logout_view,
            account_view,
            signup_view )
        
        
urlpatterns  = [
    path('signup/',signup_view, name="signup" ),
    path('logout/',logout_view, name="logout" ),
    path('login/',login_view, name="login" ),
    path('home/',home, name="home" ),
    path('profile/',account_view, name="account" ),
]