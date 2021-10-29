import json
from .models import *



def getCookieCart(request):

    """This function gets cart information from the
       cookies, for unauthenticated users
    """

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cart_products = order['get_cart_items']

    try:
        cart = json.loads(request.COOKIES['cart'])

        for item in cart:

            try:
                cart_products += cart[item]["quantity"]
                product = Product.objects.get(id = item)
                total = product.price * cart[item]["quantity"]
                order['get_cart_total'] += total
                order['get_cart_items'] += cart[item]["quantity"]

                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'image1URL': product.image1URL
                    },
                    'quantity': cart[item]['quantity'],
                    'get_total': total,
                }

                items.append(item)
            except:
                pass

    except:
        cart = {}

    return {'items': items, 'order': order, 'cart_products': cart_products}



def getCart(request):

    """This function parses cart details from the cookies using the getCookieCart function"""

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderproduct_set.all()
        cart_products = order.get_cart_items
    else:
        cookie_cart = getCookieCart(request)
        items = cookie_cart['items']
        order = cookie_cart['order']
        cart_products = cookie_cart['cart_products']
        for i in items:
            i['product']['discounted_price'] = Product.objects.get(id = i['product']['id']).discounted_price

    return {'items': items, 'order': order, 'cart_products': cart_products}



def createGuestOrder(request, data):

    """This function creates an order for an unregistered user"""

    name = data['form']['name']
    email = data['form']['email']

    cookie_cart = getCookieCart(request)
    items = cookie_cart['items']

    customer, created = Customer.objects.get_or_create(email = email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer = customer, complete = False)

    for item in items:

        product = Product.objects.get(id = item['product']['id'])
        order_product = OrderProduct.objects.create(product = product, order = order, quantity = item['quantity'])

    return customer, order
