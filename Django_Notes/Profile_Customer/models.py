from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# for my product information

CATEGORY_CHOICES = [
    ("shirt", "Shirt"),
    ("pant", "Pant"),
    ("borka", "Borka"),
    ("kids", "Kids"),
    ("shoes", "Shoes"),
]


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    image = models.ImageField(upload_to="productImages/")
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


DISTRICT_CHOICES = [
    ("Dhaka", "Dhaka"),
    ("Chittagong", "Chittagong"),
    ("Khulna", "Khulna"),
    ("Rajshahi", "Rajshahi"),
    ("Barisal", "Barisal"),
    ("Sylhet", "Sylhet"),
    ("Rangpur", "Rangpur"),
    ("Mymensingh", "Mymensingh"),
]


# for customer information as profile
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    district = models.CharField(choices=DISTRICT_CHOICES, max_length=100)
    thana = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    village = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


# for cart and order information
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"], name="unique_product_per_cart"
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
