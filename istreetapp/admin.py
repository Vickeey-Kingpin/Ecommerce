from django.contrib import admin
from . models import Item,CartItem,Order,Blog,Address,Payment,Testimonial,Refund


# Register your models here.
def confirm_payment(modeladmin,request,queryset):
    queryset.update(is_paid=True)
confirm_payment.short_description = 'Confirm payment'

def refund_granted_accepted(modeladmin,request,queryset):
    request.update(refund_requested=False,refund_granted=True)
refund_granted_accepted.short_description = 'Make refund granted'  


class addressModel(admin.ModelAdmin):
    list_display = ['user','home_address','apartment_address','country','region','address_type','default']

class orderModel(admin.ModelAdmin):
    list_display = ['user','shipping_fee','ordered','shipping_address','billing_address','payment','refund_code','refund_requested','refund_granted']
    actions = [refund_granted_accepted]

class orderPayment(admin.ModelAdmin):
    list_display = ['user','payment_option','amount_paid','is_paid','payment_number']
    actions = [confirm_payment]

admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(Order,orderModel)
admin.site.register(Blog)
admin.site.register(Address,addressModel)
admin.site.register(Payment,orderPayment)
admin.site.register(Testimonial)
admin.site.register(Refund)

