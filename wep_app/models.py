
from django.db.models import *
from datetime import datetime

# Create your models here.
class Prodect(Model):
    name = CharField(max_length=150, null = False, blank = False)
    model = CharField(max_length=150, null = True, blank = True)
    image = ImageField(upload_to = "Pictures", null = False)
    category = CharField(max_length=150, null = False, blank = False)
    brand = CharField(max_length=150, null = False, blank = False)
    price = DecimalField(max_digits=10, decimal_places=2)
    stock = BooleanField(default=False, help_text = "0-Show, 1-Hidden")
    added = CharField(max_length=150, null = True, default = "not_added") # 1.added_wish, 2.added_cart, 3.not_added
    def __str__(self):
        return self.name


class Cart(Model):
    customer = CharField(max_length = 30 , null = True)  
    image = ImageField(upload_to = "cart_img", null = True)
    name = ForeignKey(Prodect, null = False, on_delete = CASCADE)
    price = DecimalField(max_digits=10, decimal_places=2, null = True)
    quantity = IntegerField(default = 1, null = False) 
    order = BooleanField(default=False, help_text = "0-Add, 1-Remove")
    order_status = CharField(max_length=40, null=False, blank=False, default='not_order')#1.new_order, 2.old_order, 3.not_order 
    #date =DateTimeField(default=datetime.now, blank=True)


class Orderby(Model):
    customer = CharField(max_length = 30 , null = True) 
    ordered_things =  ManyToManyField(Cart)
    order_status = CharField(max_length=40, null=False, blank=False, default='bending')
    #date =DateTimeField(default=datetime.now, blank=True)
    '''
    1.success, 2.bending, 3.cancel
    '''

class user(Model):
    first_name = CharField(max_length=150, null = False, blank = False)
    last_name = CharField(max_length=150, null = False, blank = False)
    address = CharField(max_length=150, null = False, blank = False)
    city = CharField(max_length=150, null = False, blank = False)
    dist = CharField(max_length=150, null = False, blank = False)
    state = CharField(max_length=150, null = False, blank = False)
    pincode = IntegerField(null  = True)
    phone = IntegerField(null  = True)
    mail = EmailField(max_length=15, null = True)
    order = ForeignKey(Orderby, null = False, on_delete = CASCADE) 

class Wishlist(Model):
    customer = CharField(max_length = 30 , null = True)  
    image = ImageField(upload_to = "cart_img", null = True)
    name = ForeignKey(Prodect, null = False, on_delete = CASCADE)
    price = DecimalField(max_digits=10, decimal_places=2, null = True)
    quantity = IntegerField(default = 1, null = False) 
    order = BooleanField(default=False, help_text = "0-Add, 1-Remove") 