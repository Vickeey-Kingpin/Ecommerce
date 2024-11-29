from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils import timezone, formats
from django_countries.fields import CountryField

# Create your models here.
CATEGORY = (
    ('Iphone','PH'),
    ('Ipad','PD'),
    ('Iwatch','WA'),
    ('Others','OT'),
)
ADDRESS_TYPE = (
    ('Billing','B'),
    ('Shipping','S')
)

PAYMENT_OPTIONS = (
    ('Paypal','P'),
    ('Mpesa','M'),
)


class Item(models.Model):
    title = models.CharField(max_length=250)
    old_price = models.FloatField(blank=True,null=True)
    new_price = models.FloatField()
    category = models.CharField(choices=CATEGORY,max_length=10)
    description = models.CharField(max_length=500)
    image = models.ImageField(blank=True,null=True,upload_to='images/')

    def get_percentage_discount(self):
        if self.old_price:
            discount = (self.old_price-self.new_price)
            percentage_discount = (discount/self.old_price)*100
            return round(percentage_discount)
        else:
            return 0
    
    def get_absolute_url(self):
        return reverse('product', kwargs={'pk':self.pk})

    def add_to_cart(self):
        return reverse('add-to-cart', kwargs={'pk':self.pk})
    
    def add_single_to_cart(self):
        return reverse('add-single-to-cart',kwargs={'pk':self.pk})
    
    def remove_single_from_cart(self):
        return reverse('remove-single-from-cart',kwargs={'pk':self.pk})
    
    def remove_from_cart(self):
        return reverse('remove-from-cart',kwargs={'pk':self.pk})
    
    def get_amount_saved(self):
        if self.old_price:
            amount_saved = (self.old_price-self.new_price)
            return round(amount_saved)
        else:
            return self.new_price
        
    def __str__(self):
        return self.title
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} {'of'} {self.item.title}"
    
    def get_subtotal(self):
        return self.item.new_price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    shipping_fee = models.FloatField(default=0)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment= models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    refund_code = models.CharField(max_length=20,blank=True,null=True)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def get_total(self):
        total = 0
        for cart_items in self.items.all():
            total += cart_items.get_subtotal()
        return total
    
    def total_plus_shipping(self):
        return self.get_total() + self.shipping_fee

    def __str__(self) :
        return self.user.email

class Blog(models.Model):
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    date_created = models.DateField(default=timezone.now)
    image = models.ImageField(blank=True,null=True,upload_to='images/')
    

    def get_absolute_url(self):
        return reverse('blog-datail', kwargs={'pk':self.pk})
     
    def go_back_to_blog(self):
        return reverse('blog')

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    home_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    # country = models.ForeignKey(
    #     'cities_light.Country', 
    #     on_delete=models.SET_NULL, null=True, blank=True,
    #     limit_choices_to=models.Q(name__in=["Kenya", "Uganda", "Tanzania"])
    # ) 
    country = CountryField(multiple=False)
    region = models.CharField(max_length=100)
    address_type = models.CharField(max_length=20,choices=ADDRESS_TYPE)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name_plural = 'Addresses'

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_option = models.CharField(max_length=10, choices=PAYMENT_OPTIONS)
    amount_paid = models.FloatField(default=0)
    is_paid = models.BooleanField(default=False)
    payment_number = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.user.email

class Testimonial(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField(null=True,blank=True)

class Refund(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    reasons = models.TextField(null=True,blank=True)
    accepted = models.BooleanField(default=False)
    email = models.EmailField()