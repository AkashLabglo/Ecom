from contextlib import redirect_stderr
from ssl import create_default_context
from unicodedata import name
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
from datetime import datetime

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
        opj.added = "added_cart"
        opj.save()

        addCart_value, success_created = Cart.objects.get_or_create(
            name = opj,
            price = opj.price,
            image = opj.image, 
            order = False, 
            customer = request.user 
               
        )
        print(opj)
        if success_created:
            messages.info(request,'The item was added to your Cart')
        else:
            messages.info(request,'The item was already in your Cart')   
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
    if request:
        opj = Cart.objects.get(id = id)

        opj1 = Prodect.objects.get(id = opj.name.id)
        opj1.added = "not_added"
        opj1.save()

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

# check_out as order by:
'''@login_required
def Orderedby(request, id):
    my_list = [3, 5, 6, 8, 10]
    if request.method == 'POST':   
        opj = Cart.objects.get(id = id)

        # <--- tax_calculate Codes --->
        random_tax = Decimal(random.choice(my_list))
        tax_ammount = random_tax/Decimal(100) * opj.price
        tax = tax_ammount/opj.price * Decimal(100) 
        total = (tax + opj.price) * opj.quantity
        ##########################################
        tax = Decimal(18)/opj.price * Decimal(100)
        total = (tax + opj.price) * opj.quantity
        # order_tb_save:-
        addorders_values = Orderby.objects.get_or_create(
            prodect_name = opj,  
            tax = tax, 
            current_price = opj.price,
            total = total, 
            customer = opj.customer
            
        )[0]
        if opj is not None and request.method == 'POST':
            opj.order = True
            opj.save()
            opj1 = Orderby.objects.filter(prodect_name = opj)
            return render(request, "order.html" , {'opj1':opj1})
        else:
             pass        
    else:
        return HttpResponse("<h1>you not checkout prodect's</h1>")'''


@login_required
def Orderedby(request):
    ak = Prodect.objects.all()
    ak.update(added = 'not_added')
    if request.method == 'POST' : 
        opj = Cart.objects.filter(
            customer = request.user, 
           
        )
        
        taxes = 0
        for i in opj.all():
            tax = int(i.price/ 18 )
            taxes += tax
        total = opj.aggregate(Sum('price'))

        opj2= Orderby.objects.create(
            customer = request.user, 
             
            
        )      
        opj2.ordered_things.add(
            *Cart.objects.filter(Q(customer = request.user) & Q(order = False))
            #*opj 
        )
        opj.update(order = True)
        opj1 = opj2.ordered_things.all()
        print(opj1)
        contaxt = {
            'opj1':opj1, 
            'tax':tax,
            'total': total['price__sum'] + taxes
            
        }
        opj.update(order = True)
        
        return render(request, "order.html" , contaxt)

    # order_view:-    
    if request:
        opj2= Orderby.objects.latest(
            'ordered_things__id' 
        )
        
        opj1 = opj2.ordered_things.all()
        total = opj2.ordered_things.aggregate(Sum('price')) 
        quantity = opj2.ordered_things.aggregate(Sum('quantity'))
        print(total)
        print(quantity)
        #total = Orderby.objects.filter(customer = request.user).aggregate(Sum('ordered_things__price'))
        print(total)
        #tax = total['ordered_things__price__sum']/18
        tax = total['price__sum']/18
        print(int(tax))
        contaxt = {
            'opj1':opj1, 
            #'total':total['ordered_things__price__sum'] + int(tax),
            'total':total['price__sum'] * quantity['quantity__sum'] + int(tax),
            'tax':int(tax) 
            
        }
        return render(request, "orderview_page.html" , contaxt)
        

#------------------------------------------------------

# add_to_wish;-

def add_wish(request, pk):
    if request:
        
        opj = Prodect.objects.get(id = pk)
        opj.added = "added_wish"
        opj.save()

        addCart_value, success_created = Wishlist.objects.get_or_create(
            name = opj,
            price = opj.price,
            image = opj.image, 
            order = False, 
            customer = request.user 
               
        )
        print(opj)
        if success_created:
            #messages.info(request,'The item was Already in your Cart')
            messages.info(request,'The item was added to your WishList')
        else:
            messages.warning(request,'The item was Already to your WishList')    
        return redirect("interface")
    else:
        return HttpResponse("<h1>Prodects Not Added to Cart</h1>")         

# wish_Show :-

def Show_wish(request):
    '''
    >> remove your separate wish prodect's <<
    '''
    opj = Wishlist.objects.filter(
        order = False, 
        customer = request.user
        )
    return render (request, 'wish.html', {'opj': opj})

# wish_remove:-
def wish_remove(request, id):
    '''
    >> remove your separate wish prodect's <<
    '''
    opj = Wishlist.objects.get(id = id)

    opj1 = Prodect.objects.get(id = opj.name.id)
    opj1.added = "not_added"
    opj1.save()
    #messages.warning(request,'The item was Already to your WishList')    

    opj.delete()
    return redirect("Show_wish") 

#------------------------------------------------------



        
        



