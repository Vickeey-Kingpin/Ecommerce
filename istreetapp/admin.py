from django.contrib import admin
from . models import Item,CartItem,Order,Blog,Address,Payment


# Register your models here.
def confirm_payment(modeladmin,request,queryset):
    queryset.update(is_paid=True)
confirm_payment.short_description = 'Confirm payment'


class itemOrder(admin.ModelAdmin):
    list_display = ['pk','id']

class addressModel(admin.ModelAdmin):
    list_display = ['user','home_address','apartment_address','country','region','address_type','default']

class orderModel(admin.ModelAdmin):
    list_display = ['user','shipping_fee','ordered','shipping_address','billing_address']

class orderPayment(admin.ModelAdmin):
    list_display = ['user','payment_option','amount_paid','is_paid']
    actions = [confirm_payment]

admin.site.register(Item,itemOrder)
admin.site.register(CartItem)
admin.site.register(Order,orderModel)
admin.site.register(Blog)
admin.site.register(Address,addressModel)
admin.site.register(Payment,orderPayment)
