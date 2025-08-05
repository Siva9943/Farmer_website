from django.shortcuts import render,redirect
from sells_core.forms import SellerProductForm
from sells_core.models import *
from core.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
#seller add product
def seller_add_product(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            seller = Seller.objects.filter(user=request.user).first()
            if not seller:
                messages.error(request, "Seller profile not found.")
                print("Seller not found for user:", request.user)
                return redirect('seller_dashboard')

            print("Creating product for seller:", seller)
            product = SellerProduct.objects.create(
                seller=seller,
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                price=request.POST.get('price'),
                quantity=request.POST.get('quantity'),
                image=request.FILES.get('image')
            )
            print("Product created:", product.name)
            messages.success(request, "Product added successfully.")
            return redirect('view_products')
        else:
            return redirect('add_product')

    return render(request, 'seller/add_product.html',{'active_page': 'sell'})


def view_products(request):
    obj = SellerProduct.objects.all() 
    print(obj)
    context = {
        'products': obj,
        'active_page': 'products'
    }
    print(context)
    return render(request, 'seller/view_product.html', context)


def edit_product(request, product_id):
    product = get_object_or_404(SellerProduct, id=product_id, seller__user=request.user)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        messages.success(request, "Product updated successfully.")
        return redirect('view_products')

    return render(request, 'seller/edit_product.html', {'product': product})


def delete_product(request, product_id):
    product = get_object_or_404(SellerProduct, id=product_id, seller__user=request.user)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('view_products')

def view_orders(request):
    return render(request, 'seller/orders.html', {'active_page': 'order'})
 