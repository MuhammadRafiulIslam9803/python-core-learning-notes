from django.contrib import messages
from django.http import request
from django.shortcuts import redirect, render
from django.views import View

from .forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm
from django.contrib.auth.views import LogoutView

from .models import Customer, Product, Cart, CartItem
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


# home page view
class ProductView(View):
    def get(self, request):
        gentsPant = Product.objects.filter(category="pant")
        shirts = Product.objects.filter(category="shirt")
        borka = Product.objects.filter(category="borka")
        shoes = Product.objects.filter(category="shoes")
        return render(
            request,
            "shop/home.html",
            {"gentsPant": gentsPant, "shirts": shirts, "borka": borka, "shoes": shoes},
        )


# product details view
class ProductDetailsView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        return render(request, "shop/productDetails.html", {"product": product})


# category view
class categoryView(View):
    def get(self, request, category):
        products = Product.objects.filter(category=category)
        return render(request, "shop/category.html", {"products": products})


# customer registration view
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "shop/customerregistration.html", {"form": form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Congratulations! You have registered successfully."
            )
            return redirect("home")
        return render(request, "shop/customerregistration.html", {"form": form})


# customer logout view
class UserLogoutView(LogoutView):
    next_page = "login"

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")

        return super().dispatch(request, *args, **kwargs)


# Customer profile view
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        customer, created = Customer.objects.get_or_create(user=request.user)

        form = CustomerProfileForm(instance=customer)

        return render(request, "shop/profile.html", {"form": form})

    def post(self, request):
        customer, created = Customer.objects.get_or_create(user=request.user)

        form = CustomerProfileForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()

            messages.success(request, "Profile updated successfully!")

            return redirect("address")

        return render(request, "shop/profile.html", {"form": form})


# show profile on address page
class AddressView(View):
    def get(self, request):
        customer = Customer.objects.filter(user=request.user).first()

        return render(request, "shop/address.html", {"customer": customer})


# add to cart view
class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, id):
        product = Product.objects.get(id=id)

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, f"{product.name} has been added to your cart.")

        return redirect("cart")


# cart view
class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_items = cart.items.select_related("product")

        total = 0

        for item in cart_items:
            price = (
                item.product.discounted_price
                if item.product.discounted_price
                else item.product.price
            )

            item.subtotal = price * item.quantity
            total += item.subtotal

        return render(
            request,
            "shop/cart.html",
            {
                "cart_items": cart_items,
                "total": total,
            },
        )


# quantity remove add in cart view
class IncreaseCartView(LoginRequiredMixin, View):
    def get(self, request, id):
        cart_item = CartItem.objects.get(id=id, cart__user=request.user)

        cart_item.quantity += 1
        cart_item.save()

        return redirect("cart")


class DecreaseCartView(LoginRequiredMixin, View):
    def get(self, request, id):
        cart_item = CartItem.objects.get(id=id, cart__user=request.user)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect("cart")


class RemoveCartView(LoginRequiredMixin, View):
    def get(self, request, id):
        cart_item = CartItem.objects.get(id=id, cart__user=request.user)

        cart_item.delete()

        return redirect("cart")
