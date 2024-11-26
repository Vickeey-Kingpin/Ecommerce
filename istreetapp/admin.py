from django.contrib import admin
from . models import Item,CartItem,Order,Blog,Address


# Register your models here.
class itemOrder(admin.ModelAdmin):
    list_display = ['pk','id']

class addressModel(admin.ModelAdmin):
    list_display = ['user','home_address','apartment_address','country','region','address_type','default']

class orderModel(admin.ModelAdmin):
    list_display = ['user','shipping_fee','ordered','shipping_address','billing_address']

admin.site.register(Item,itemOrder)
admin.site.register(CartItem)
admin.site.register(Order,orderModel)
admin.site.register(Blog)
admin.site.register(Address,addressModel)
