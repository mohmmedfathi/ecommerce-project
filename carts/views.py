from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product,Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # get the product
    
    # product variation
    product_variation = []
    if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(product = product,variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
            
    # cart 
    try:
        # get the cart by cart_id that is present is session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    
    # cart item
    is_cart_item_exists = CartItem.objects.filter(product = product,cart = cart).exists()
    if is_cart_item_exists:
        
        cart_item = CartItem.objects.filter(product=product,cart = cart)
        
        existing_variations_list = []
        id_list = []
        for item in cart_item:
            existing_variations = item.variations.all()
            existing_variations_list.append(list(existing_variations))
            id_list.append(item.id)
            
        if product_variation in existing_variations_list:
            
            item_index = existing_variations_list.index(product_variation)
            item_id  = id_list[item_index]
            
            item = CartItem.objects.get(product = product,id = item_id)
            item.quantity+=1
            item.save()
            
        else:
            item = CartItem.objects.create(product = product,quantity = 1,cart = cart)   
            
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)

            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()

    return redirect('cart')

# remove one instance of cart item


def remove_cart(request, product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try : 
        cart_item = CartItem.objects.get(product=product, cart=cart,id = cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')


# remove all instances of cart item (the row)
def remove_all_cart_item(request, product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart,id =cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    Tax_Percentage = 2
    try:
        tax = 0
        net_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (total * Tax_Percentage) / 100
        net_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'net_total': net_total
    }
    return render(request, 'store/cart.html', context)
