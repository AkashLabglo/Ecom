
from django.db.models import *

# Create your models here.
class Prodect(Model):
    name = CharField(max_length=150, null = False, blank = False)
    model = CharField(max_length=150, null = True, blank = True)
    image = ImageField(upload_to = "Pictures", null = False)
    category = CharField(max_length=150, null = False, blank = False)
    brand = CharField(max_length=150, null = False, blank = False)
    price = DecimalField(max_digits=10, decimal_places=2)
    stock = BooleanField(default=False, help_text = "0-Show, 1-Hidden")
    def __str__(self):
        return self.name


class Cart(Model):
    customer = CharField(max_length = 30 , null = True)  
    image = ImageField(upload_to = "cart_img", null = True)
    name = ForeignKey(Prodect, null = False, on_delete = CASCADE)
    price = DecimalField(max_digits=10, decimal_places=2, null = True)
    quantity = IntegerField(default = 1, null = False) 
    order = BooleanField(default=False, help_text = "0-Add, 1-Remove") 


class Orderby(Model):
    customer = CharField(max_length = 30 , null = True) 
    image = ImageField(upload_to = "cart_img", null = True) 
    prodect_name = ForeignKey(Cart, null = True, on_delete = CASCADE)
    tax = DecimalField(max_digits=10, decimal_places=2, null = False)
    original_price = DecimalField(max_digits=10, decimal_places=2, null = True) 
    current_price = DecimalField(max_digits=10, decimal_places=2, null = True)
    total = DecimalField(max_digits=10, decimal_places=2, null = True)
    

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