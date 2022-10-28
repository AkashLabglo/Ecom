"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import search
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from wep_app.views import *


'''urlpatterns = [ 
    path('search', SearchResultsView.as_view(), name='search_results'),
]'''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', interface, name = "interface"),
    path('search', search, name = "search"),  
    # Cart related urls:-
    path('cart/<pk>', add_cart, name = "add_cart"), 
    path('Show_cart', Show_cart, name = 'Show_cart'), 
    path('remove/<id>', Cart_remove, name = "Car_remove"),
    path('Orderedby/<id>', Orderedby, name = "Orderedby"), #----saparate_cart prodct get url-----
    #path('Orderedby', Orderedby, name = "Orderedby"), 
    path('addquantity/<id>', addquantity, name = "addquantity"),  
    # Login/register/logout/password's_Path
    path("login", login, name = "login"),
    path('Logout', Logout, name = 'Logout'), 
    path('register', Register, name = 'register'), 
    
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)