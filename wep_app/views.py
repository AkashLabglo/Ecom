from contextlib import redirect_stderr
from django.shortcuts import render, redirect
from wep_app.models import *
from django.http import *
# genaricView_moduels:-
from django.db.models import Q
# message:-
from django.contrib import messages
# login__logout _authenticate moduels:-
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as authlogin, logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User 
# only_allowed_login person:-
from django.contrib.auth.decorators import login_required
# calulate_to use random module:-
import random
from decimal import Decimal

#------------------------------------------------------

# all_prodects & Home_page

def interface(request):
    opj = Prodect.objects.all()
    return render (request, "interface.html",{"opj":opj})
# --------------------------------------------------------

# search_box

def search(request):
   # opj =  (Prodect.objects.filter(name = request.POST.get("search")) or  Prodect.objects.filter(category = request.POST.get("search"))) and Prodect.objects.filter(stock = 0)
    opj = Prodect.objects.filter((Q(brand = request.POST.get("search")) | Q(category = request.POST.get("search")) | Q(name = request.POST.get("search"))) & Q(stock = 0))
    return render (request, 'interface.html', {'opj': opj})
# --------------------------------------------------------

# add_to_cart prodects(tb_added):-
@login_required
def add_cart(request, pk):
    if request:
        
        opj = Prodect.objects.get(id = pk)

        addCart_value = Cart.objects.create(
            name = opj,
            price = opj.price,
            image = opj.image, 
            order = False, 
            customer = request.user 
               
        )
        print(opj)
        return redirect("interface")
    else:
        return HttpResponse("<h1>Prodects Not Added to Cart</h1>")
# --------------------------------------------------------

# Cart_Show :-
@login_required
def Show_cart(request):
    opj = Cart.objects.filter(
        order = False, 
        customer = request.user
        )
    return render (request, 'Cart_view.html', {'opj': opj})

# cart_items_remove:-
@login_required
def Cart_remove(request, id):
    opj = Cart.objects.get(id = id)
    opj.delete()
    return redirect("Show_cart")    

# cart quantity_add:-
@login_required
def addquantity(request, id):
    opj = Cart.objects.get(id = id)
    #opj1 = request.POST.get('quantity')
    opj.quantity = request.POST.get('quantity')
    opj.save()
    return redirect('Show_cart')
#------------------------------------------------------

# login_Page:-

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
    
        if user is not None:
            if user.is_active:
                authlogin(request, user)
                return redirect('interface')
        else:
            return HttpResponse("Try Again")
    
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

#------------------------------------------------------

# logout_:-
@login_required
def Logout(request):
    logout(request)
    return redirect('interface')    
#------------------------------------------------------

# register_page:-

def Register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')
            user = authenticate(username=username, password=password)
            authlogin(request, user)
            return redirect('interface')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form}) 


#------------------------------------------------------

# check_out (to) order by:
@login_required
def Orderedby(request, id):
    my_list = [3, 5, 6, 8, 10]
    if request.method == 'POST':   
        opj = Cart.objects.get(id = id)

        # <--- tax_calculate Codes --->
        '''random_tax = Decimal(random.choice(my_list))
        tax_ammount = random_tax/Decimal(100) * opj.price
        tax = tax_ammount/opj.price * Decimal(100) 
        total = (tax + opj.price) * opj.quantity'''
        ##########################################
        tax = Decimal(18)/opj.price * Decimal(100)
        total = (tax + opj.price) * opj.quantity
        # order_tb_save:-
        addorders_values = Orderby.objects.create(
            prodect_name = opj,  
            tax = tax, 
            current_price = opj.price,
            total = total
            
        )
        if opj is not None and request.method == 'POST':
            opj.order = True
            opj.save()
            opj1 = Orderby.objects.filter(prodect_name = opj)
            return render(request, "order.html" , {'opj1':opj1})
        else:
             pass        
    else:
        return HttpResponse("<h1>you not checkout prodect's</h1>")   



'''def Orderedby(request):
    if request.method == 'POST': 
        opj = Cart.objects.filter(
            customer = request.user,
        )
        


        addorders_values = Orderby.objects.create(
            
            prodect_name = opj, 
            tax = tax, 
            current_price = opj.price,
            total = total, 
            customer = request.user
            
        )
        opj.update(order = True)
        opj1 = Orderby.objects.filter(
            customer = request.user
        )
        return render(request, "order.html" , {'opj1':opj1})'''
#------------------------------------------------------

'''
const[state,setState]=useState(fathers name:"")
<input name="fathers name" value="{state.father name} onchange={(e)=>setState(e.target.value)}"/>
''' 
         




               
        
        



'''def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        if search is not None:
            if search is Prodect.objects.filter(category__iexact = search):
                opj = Prodect.objects.filter(category = search)
                print(opj)
                return render (request, "prodect_tb.html", {'opj':opj})
            elif search is Prodect.objects.filter(brand = search):
                opj = Prodect.objects.filter(name = search)
                return render (request, "prodect_tb.html", {'opj':opj})
            else:
                return HttpResponse("<h1>Prodects Not Available</h1>")     
        else:
            pass
    else:
        opj = Prodect.objects.all()
        return render (request, "prodect_tb.html", {'opj':opj})'''