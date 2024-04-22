from django.contrib import admin
from django.urls import path
from  . import   views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index ,name='shopHome'),
    path('about/',views.about ,name='aboutus'),
    path('contact/',views.contact ,name='contactus'),
    path('Product/<int:myid>',views.productView ,name='productView'),
    path('tracker/',views.tracker ,name='tracker'),
    path('search/',views.search ,name='search'),
    path('checkout/',views.checkout ,name='checkout'),
    path('cartpage/',views.cartpage,name='cartpage'),
    # path('handlepayment/',views.handlepayment , name='handlepayment'),
    path('signup/',views.handleSignup , name='handleSignup'),
    path('login/' , views.handleLogin , name='handleLogin'),
    path('logout/' ,views.LogOut ,name='LogOut'),
]