from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic import ListView, DetailView,View
from . models  import Item,CartItem,Order, Blog,Address
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm

# Create your views here.
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
        # try:
        # order = Order.objects.get(user=self.request.user,ordered=False)
        context = {
        'form':form,
        }  
        shipping_address_qs = Address.objects.filter(user=self.request.user,default=True,address_type='Shipping') 
        if shipping_address_qs.exists():
            context.update({'default_shipping_address':shipping_address_qs[0]})         
        return render(self.request, 'checkout.html',context)
        # except ObjectDoesNotExist:
        #     messages.warning(self.request, 'Order does not exist')
        #     return redirect('checkout')

    def post(self, *args,**kwargs):
        form = CheckoutForm(self.request.POST or None)

        
        if form.is_valid():
            use_default_shipping = form.cleaned_data.get('use_default_shipping')
            if use_default_shipping:
                print('Using the default shippng address')
                address_qs = Address.objects.filter(user=self.request.user,address_type='Shipping',default=True)
                if address_qs.exists():
                    shipping_address = address_qs[0]
                    
                else:
                    messages.info(self.request, "No default shipping address available")
                    return redirect('checkout')
            else:
                print("User is entering a new billing address")
                home_address = form.cleaned_data.get('shipping_home')
                apartment_address = form.cleaned_data.get('shipping_apartment')
                country = form.cleaned_data.get('shipping_country')
                region = form.cleaned_data.get('shipping_region')
                # set_default_shipping = form.cleaned_data.get('set_default_shipping')
                
                shipping_address = Address(
                    user=self.request.user,
                    home_address = home_address,
                    apartment_address = apartment_address,
                    country = country,
                    region = region,
                    address_type= 'Shipping',
                    )
                shipping_address.save()

                set_dafault_shipping = form.cleaned_data.get('set_dafault_shipping')
                if set_dafault_shipping:
                    shipping_address.default = True
                    shipping_address.save()

                return redirect('checkout')        
        else:    
            print(form.errors)
            messages.warning(self.request, 'Form contains errors.')
            return redirect('checkout')
