from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
from .models import *
import datetime
from .utils import getCart, createGuestOrder
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm, UploadForm, DeleteUser
from .filters import CatalogFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string



def shop(request):

    """Shop view, handles display of products, filtering
       and pagination
    """

    data = getCart(request)
    cart_products = data['cart_products']
    products = Product.objects.all()

    # Check if user wants to sort by name or price

    dict = request.GET.dict()

    params = ""

    for k, v in dict.items():
        if k != "page":
            params += "&" + str(k) + "=" + str(v)

    if request.method == 'GET':
        catalog_filter = CatalogFilter(request.GET, queryset = products) # get query filters from the form
        products = catalog_filter.qs

    if "SortByName" in request.GET and "SortByPrice" in request.GET:
        if request.GET["SortByPrice"] == "Ascending" and request.GET["SortByName"] == "Ascending":
            products = sorted(products, key = lambda p: (p.discounted_price, p.name))
        elif request.GET["SortByPrice"] == "Descending" and request.GET["SortByName"] == "Ascending":
            products = sorted(products, key = lambda p: (-p.discounted_price, p.name))
        elif request.GET["SortByPrice"] == "Descending" and request.GET["SortByName"] == "Descending":
            products = sorted(products, key = lambda p: (p.discounted_price, p.name), reverse = True)
        elif request.GET["SortByPrice"] == "Ascending" and request.GET["SortByName"] == "Descending":
            products = sorted(products, key = lambda p: (-p.discounted_price, p.name), reverse = True)
    else:

        if "SortByName" in request.GET:

            if request.GET["SortByName"] == "Ascending":
                products = sorted(products, key = lambda p: p.name)
            else:
                products = sorted(products, key = lambda p: p.name, reverse = True)

        if "SortByPrice" in request.GET:
            if request.GET["SortByPrice"] == "Ascending":
                products = sorted(products, key = lambda p: p.discounted_price)
            else:
                products = sorted(products, key = lambda p: p.discounted_price, reverse = True)

    # Provide pagination

    products = Paginator(products, 8)
    pages = products.num_pages
    page_num = int(request.GET.get("page", 1))

    try:
        products = products.page(page_num)
    except:
        products = products.page(1)

    context = {
        'products': products, 
        'cart_products': cart_products, 
        'catalog_filter': catalog_filter,
        'page_num': page_num, 
        'pages': pages, 
        'params': params
    }

    return render(request, 'shop/shop.html', context)



def product(request):

    """Product view, displays product and all details
    
    """

    data = getCart(request)
    items = data['items']
    order = data['order']
    cart_products = data['cart_products']

    product = Product.objects.filter(id = request.GET.get("product")).first()

    context = {
        'cart_products': cart_products, 
        'product': product
    }

    return render(request, 'shop/product.html', context)



def cart(request):

    """Cart view, displays a list of products currently in cart,
       quantity, price and total
    """


    data = getCart(request)
    items = data['items']
    order = data['order']
    cart_products = data['cart_products']

    context = {
        'items': items, 
        'order': order, 
        'cart_products': cart_products
    }

    return render(request, 'shop/cart.html', context)



def updateProduct(request):

    """This function increases or decreases product quantity;
       when it reaches 0, it's deleted
    """

    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id = product_id)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    order_product, created = OrderProduct.objects.get_or_create(order = order, product = product)

    if action == 'add':
        order_product.quantity = order_product.quantity + 1
    elif action == 'remove':
        order_product.quantity = order_product.quantity - 1

    order_product.save()

    if order_product.quantity <= 0:
        order_product.delete()

    return JsonResponse('Product was added', safe = False)


@csrf_exempt
def processOrder(request):

    """This function checks if the user is authenticated or not;
       if he is, data is fetched from the database, otherwise
       it's fetched via the form
    """

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    print(data)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)

    else:
        customer, order = createGuestOrder(request, data)
        ShippingInfo.objects.get_or_create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            county = data['shipping']['county'],
            zipcode = data['shipping']['zipcode'],
        )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True

        message = render_to_string('shop/order_completion_email.html', {'first_name': request.POST.get('first_name')})

        send_mail("Order #"+str(order.id), 
            message, settings.EMAIL_HOST_USER,
            [request.POST.get('email')], 
            fail_silently = True
        )

    order.save()

    return JsonResponse('Payment complete', safe = False)


def checkout(request):

    """Checkout view
    """

    

    data = getCart(request)
    items = data['items']
    order = data['order']
    cart_products = data['cart_products']

    context = {
        'items': items, 
        'order': order, 
        'cart_products': cart_products,
    }

    if request.user.is_authenticated:
        customer = request.user.customer

        shipping_info = ShippingInfo.objects.get(customer = customer)

        name = str(request.user.customer.first_name) + " " + str(request.user.customer.last_name)
        context['shipping_info'] = shipping_info
        context['name'] = name

    return render(request, 'shop/checkout.html', context)



def login_page(request):

    """User login (available only if unauthenticated)
    """

    if request.user.is_authenticated:
        return redirect('shop')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('shop')
            else:
                messages.info(request, "Username doesn't match password.")

        context = {}

        return render(request, 'shop/login_page.html', context)


def registration_page(request):

    """User registration (available only if unauthenticated)"""


    if request.user.is_authenticated:
        return redirect('shop')
    else:
        register_form = RegistrationForm()

        if request.method == 'POST':
            register_form = RegistrationForm(request.POST)

            if register_form.is_valid():

                user = register_form.save()

                customer = Customer(
                    user = user, 
                    first_name = request.POST.get('first_name'), 
                    last_name = request.POST.get('last_name'), 
                    email = request.POST.get('email'), 
                    image = "default_profile_pic.jpg"
                )
                customer.save()

                shipping = ShippingInfo(
                    customer = customer, 
                    address = request.POST.get('address'), 
                    city = request.POST.get('city'), 
                    county = request.POST.get('county'), 
                    zipcode = request.POST.get('zipcode')
                )
                shipping.save()

                message = render_to_string('shop/confirmation_email.html', {'first_name': request.POST.get('first_name')})

                send_mail('PC E-shop account registration', 
                    message, settings.EMAIL_HOST_USER,
                    [request.POST.get('email')], 
                    fail_silently = True
                )

                messages.success(request, 'You can now login.')

                return redirect('login_page')

        context = {
            'register_form': register_form
        }

        return render(request, 'shop/registration_page.html', context)


def Logout(request):

    logout(request)

    return redirect('shop')


def profile_page(request):

    if not request.user.is_authenticated:

        return redirect('login_page')
    else:

        context = {}
        upload_form = UploadForm()

        if request.method == 'POST':
            upload_form = UploadForm(request.POST, request.FILES)

            if upload_form.is_valid():
                request.user.customer.image.delete(save = False)
                request.user.customer.image = request.FILES['image']
                request.user.customer.save()

                context['upload_form'] = upload_form

                messages.success(request, 'Image successfully uploaded.')

                return redirect('profile_page')

        data = getCart(request)
        cart_products = data['cart_products']

        shipping_address = ShippingInfo.objects.filter(customer = request.user.customer).first()

        context = {
            'cart_products': cart_products,
            'upload_form': upload_form, 
            'shipping_address': shipping_address
        }

        return render(request, 'shop/profile_page.html', context)


def Delete(request):

    """Delete profile view, user is asked if he still
       wishes to proceed; if confirmed, user profile
       will be deleted forever
    """

    context = {}

    if not request.user.is_authenticated:

        return redirect('shop')

    else:

        context = {}

        delete_user = DeleteUser()

        delete_user.fields['username'].initial = request.user.id

        context['delete_user'] = delete_user

        if request.method == 'POST':

            delete_user = DeleteUser(request.POST)

            delete_user.fields['username'].initial = request.user.id

            context['delete_user'] = delete_user

            if delete_user.is_valid():

                ShippingInfo.objects.get(customer = customer).delete()

                User.objects.get(id = delete_user.fields['username'].initial).delete()

                return redirect('shop')

        return render(request, 'shop/delete.html', context)



def reset_back(request):

    return redirect('shop')



def error_404(request, exception):

    data = getCart(request)
    cart_products = data['cart_products']

    context = {
        'cart_products': cart_products
    }

    return render(request, 'shop/404.html', context)

def privacy_policy(request):

    data = getCart(request)
    cart_products = data['cart_products']

    context = {
        'cart_products': cart_products
    }

    return render(request, 'shop/privacy_policy.html', context)



def cookie_policy(request):

    data = getCart(request)
    cart_products = data['cart_products']

    context = {
        'cart_products': cart_products
    }

    return render(request, 'shop/cookie_policy.html', context)