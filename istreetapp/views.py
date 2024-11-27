from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic import ListView, DetailView,View
from . models  import Item,CartItem,Order, Blog,Address
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm

# Create your views here.
def check_form_validity(values):
    valid = True
    for field in values:
        if field == '':
            valid=False
    return valid

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if len(password) >= 8:
                if User.objects.filter(email=email).exists():
                    messages.warning(request, 'This email already exist')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=email,email=email,first_name=firstname,last_name=lastname,password=password)
                    user.save()
                    messages.success(request, 'Regiser Successifully. Log in here')
                    return redirect('login')
            else:
                messages.warning(request, 'Password must contain atleast 8 characters')
                return redirect('register')
        else:
            messages.warning(request, 'Password does not match')
            return redirect('register')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=email,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request, 'Login Successifull')
            return redirect('/')
        else:
            messages.warning(request, 'Invalid email or password')
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

class HomeView(ListView):
    model = Item
    template_name = 'home.html'

class ProductView(DetailView):
    model = Item
    template_name = 'product.html'

class ShopView(ListView):
    model = Item
    template_name = 'shop.html'

class BlogView(ListView):
    model = Blog
    template_name = 'blog.html'

def contactview(request):
    return render(request,'contact.html')

def aboutview(request):
    return render(request,'about.html')

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'detailed-blog.html'

class CartView(ListView):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = {
                'object':order
            }
            return render(self.request, 'cart.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You don\'t have an active order')
            return redirect('/')

@login_required
def add_to_cart(request,pk):
    item = get_object_or_404(Item,pk=pk)
    cart_item, created = CartItem.objects.get_or_create(item=item,user=request.user)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            messages.info(request, 'This item already exists in your Cart')
        else:
            order.items.add(cart_item)
            messages.success(request, 'This item is successifully added to your cart')
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(cart_item)
        messages.success(request, 'Order created successifull. You can view your cart')
    return redirect('product',pk=pk)

@login_required
def add_single_to_cart(request,pk):
    item = get_object_or_404(Item,pk=pk)
    try:
        cart_item = CartItem.objects.get(item=item,user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart')
    except ObjectDoesNotExist:
        messages.info(request, 'Object not founnd')
        return redirect('cart')
    
@login_required
def remove_single_from_cart(request,pk):
    item = get_object_or_404(Item,pk=pk)
    order = Order.objects.get(ordered=False,user=request.user)
    try:
        cart_item = CartItem.objects.get(item=item,user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            order.items.remove(cart_item)
            cart_item.delete()
            messages.success(request,'This item successifully removed from your cart')
        return redirect('cart')
    except ObjectDoesNotExist:
        messages.info(request, 'Object not founnd')
        return redirect('cart')

@login_required    
def remove_item_from_cart(request,pk):
    item = get_object_or_404(Item,pk=pk)
    cart_item = CartItem.objects.get(item=item,user=request.user)
    order = Order.objects.get(ordered=False,user=request.user)
    order.items.remove(cart_item)
    cart_item.delete()
    messages.success(request,'This item successifully removed from your cart')
    return redirect('cart')

class CheckOutView(View):
    def get(self,*args,**kwargs):
        form = CheckoutForm()
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = {
            'form':form,
            }  
            shipping_address_qs = Address.objects.filter(user=self.request.user,default=True,address_type='Shipping') 
            if shipping_address_qs.exists():
                context.update({'default_shipping_address':shipping_address_qs[0]})   
            billing_address_qs = Address.objects.filter(user=self.request.user,default=True,address_type='Billing')
            if billing_address_qs.exists():
                context.update({'default_billing_address':billing_address_qs[0]})   
            return render(self.request, 'checkout.html',context)
            
        except ObjectDoesNotExist:
            messages.warning(self.request, 'Order does not exist')
            return redirect('checkout')

    def post(self, *args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)

            if form.is_valid():
                # Shipping Address
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    print('Using the default shippng address')
                    address_qs = Address.objects.filter(user=self.request.user,address_type='Shipping',default=True)
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request, "No default shipping address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new billing address")
                    home_address = form.cleaned_data.get('shipping_home')
                    apartment_address = form.cleaned_data.get('shipping_apartment')
                    country = form.cleaned_data.get('shipping_country')
                    region = form.cleaned_data.get('shipping_region')
                    
                    if check_form_validity([home_address,apartment_address,country,region]):
                        shipping_address = Address(
                            user=self.request.user,
                            home_address = home_address,
                            apartment_address = apartment_address,
                            country = country,
                            region = region,
                            address_type= 'Shipping',
                            )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_dafault_shipping = form.cleaned_data.get('set_dafault_shipping')
                        if set_dafault_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.warning(self.request, "Please fill in the required shipping address fields to continue")
                        return redirect('checkout') 
                    return redirect('checkout') 

                # Billing Address
                use_default_billing = form.cleaned_data.get('use_default_billing')
                shipping_same_billing = form.cleaned_data.get('shipping_same_billing')
                
                if shipping_same_billing:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'Billing'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()
                elif use_default_billing:
                    print('Using the default billing address')
                    address_qs = Address.objects.filter(user=self.request.user,address_type='Billing',default=True)
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request, "No default billing address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new billing address")
                    billing_home_address = form.cleaned_data.get('billing_home')
                    billing_apartment_address = form.cleaned_data.get('billing_apartment')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_region = form.cleaned_data.get('billing_region')
                    
                    if check_form_validity([billing_home_address,billing_apartment_address,billing_country,billing_region]):
                        billing_address = Address(
                            user=self.request.user,
                            home_address = billing_home_address,
                            apartment_address = billing_apartment_address,
                            country = billing_country,
                            region = billing_region,
                            address_type= 'Billing',
                            )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_dafault_billing = form.cleaned_data.get('set_dafault_billing')
                        if set_dafault_billing:
                            billing_address.default = True
                            billing_address.save()
                    else:
                        messages.warning(self.request, "Please fill in the required billing address fields to continue")
                    return redirect('checkout') 
                return redirect('checkout') 

            else:    
                print(form.errors)
                messages.warning(self.request, 'Form contains errors.')
                return redirect('checkout')
        except ObjectDoesNotExist:
            messages.info(self.request, 'Order does not exist')
            return redirect('checkout')

class RefundView(ListView):
    model = Blog
    template_name = 'refund.html'