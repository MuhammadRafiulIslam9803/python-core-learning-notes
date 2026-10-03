# Django Cart System — Step 2: Add to Cart

## আমাদের লক্ষ্য

STEP 1-এ আমরা তৈরি করেছি:

```text
User
  ↓
Cart
  ↓
CartItem
  ↓
Product
```

এখন আমরা Product Details page-এর **Add to Cart** button কাজ করাব।

আমাদের expected flow:

```text
User Product Details page-এ যাবে
          ↓
      Add to Cart
          ↓
     Product ID
          ↓
    Product খুঁজবে
          ↓
 User-এর Cart খুঁজবে/তৈরি করবে
          ↓
Product Cart-এ আগে আছে?
       ↙       ↘
     না          হ্যাঁ
     ↓            ↓
CartItem তৈরি   Quantity + 1
       ↘        ↙
          ↓
       Success Message
          ↓
Product Details page
```

---

# STEP 2.1 — Cart এবং CartItem Import

প্রথমে `views.py`-তে models import করতে হবে।

আগে যদি থাকে:

```python
from .models import Customer, Product
```

তাহলে পরিবর্তন করে:

```python
from .models import Customer, Product, Cart, CartItem
```

---

## কেন import করতে হবে?

আমরা `AddToCartView`-এর মধ্যে `Cart` এবং `CartItem` ব্যবহার করব।

যেমন:

```python
Cart.objects.get_or_create(...)
```

এবং:

```python
CartItem.objects.get_or_create(...)
```

Python-কে আগে জানাতে হবে `Cart` এবং `CartItem` কোন model।

তাই:

```python
from .models import Customer, Product, Cart, CartItem
```

---

# STEP 2.2 — AddToCartView তৈরি

`ProductDetailsView`-এর নিচে:

```python
class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, id):
        product = Product.objects.get(id=id)

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(
            request,
            f"{product.name} has been added to your cart."
        )

        return redirect("productDetails", id=product.id)
```

এখন এটাকে line by line বুঝি।

---

# 1. `LoginRequiredMixin`

```python
class AddToCartView(LoginRequiredMixin, View):
```

এখানে:

```python
LoginRequiredMixin
```

ব্যবহার করার অর্থ:

**শুধু logged-in user Add to Cart করতে পারবে।**

যদি user login না করে:

```text
Product Details
      ↓
 Add to Cart
      ↓
Login Required
      ↓
Login Page
```

অর্থাৎ guest user সরাসরি Cart-এ product add করতে পারবে না।

---

# 2. `View`

```python
class AddToCartView(LoginRequiredMixin, View):
```

`View` হলো Django-এর class-based view-এর base class।

আমরা এর মধ্যে:

```python
def get(...)
```

লিখে request handle করছি।

---

# 3. `get(self, request, id)`

```python
def get(self, request, id):
```

এখানে তিনটি গুরুত্বপূর্ণ জিনিস আছে:

### `self`

Class-এর current object বোঝায়।

### `request`

Browser থেকে আসা request।

এর মাধ্যমে আমরা logged-in user পেতে পারি:

```python
request.user
```

### `id`

URL থেকে product-এর ID আসবে।

যেমন URL:

```text
/product/7/add-to-cart/
```

তাহলে:

```text
id = 7
```

---

# 4. Product খুঁজে বের করা

```python
product = Product.objects.get(id=id)
```

ধরো URL:

```text
/product/7/add-to-cart/
```

তাহলে:

```python
id = 7
```

এবং Django database থেকে খুঁজবে:

```text
Product
ID = 7
```

তারপর সেটাকে:

```python
product
```

variable-এর মধ্যে রাখবে।

অর্থাৎ:

```text
URL
 ↓
id = 7
 ↓
Product.objects.get(id=7)
 ↓
product
```

---

# Important: `objects.get()`

```python
Product.objects.get(id=id)
```

মানে:

**database থেকে এমন একটি Product খুঁজে দাও যার id URL-এর id-এর সমান।**

যদি Product পাওয়া যায় → product পাওয়া যাবে।

যদি Product না পাওয়া যায় → exception/error হতে পারে।

তাই পরে আমরা আরও safe version ব্যবহার করব:

```python
from django.shortcuts import get_object_or_404
```

তারপর:

```python
product = get_object_or_404(Product, id=id)
```

এটা invalid ID হলে সুন্দরভাবে 404 response দেবে।

---

# 5. User-এর Cart খুঁজে বের করা

```python
cart, created = Cart.objects.get_or_create(
    user=request.user
)
```

এখানে খুব গুরুত্বপূর্ণ একটি Django method ব্যবহার হয়েছে:

```python
get_or_create()
```

এর কাজ:

**Object থাকলে সেটা return করবে, না থাকলে তৈরি করবে।**

---

## `request.user`

```python
request.user
```

মানে বর্তমানে যে user login করে আছে।

ধরো:

```text
Logged-in User = Rafiul
```

তাহলে:

```python
request.user
```

হবে Rafiul-এর User object।

---

# `get_or_create()` কী করছে?

```python
Cart.objects.get_or_create(
    user=request.user
)
```

Django প্রথমে দেখবে:

```text
Rafiul-এর Cart আছে?
```

### যদি Cart থাকে

তাহলে existing Cart return করবে।

```text
Rafiul
  ↓
Existing Cart
```

### যদি Cart না থাকে

নতুন Cart তৈরি করবে।

```text
Rafiul
  ↓
No Cart
  ↓
Create Cart
```

---

# `cart, created` কেন দুইটা variable?

```python
cart, created = Cart.objects.get_or_create(...)
```

`get_or_create()` সাধারণত দুইটি value return করে:

```text
object
created
```

তাই:

```python
cart
```

এর মধ্যে Cart object থাকবে।

আর:

```python
created
```

এর মধ্যে Boolean থাকবে।

### যদি নতুন Cart তৈরি হয়:

```python
created = True
```

### যদি আগের Cart পাওয়া যায়:

```python
created = False
```

উদাহরণ:

```text
Cart আগে ছিল না
→ cart = নতুন Cart
→ created = True
```

অথবা:

```text
Cart আগে থেকেই ছিল
→ cart = existing Cart
→ created = False
```

---

# 6. CartItem খুঁজে বের করা বা তৈরি করা

```python
cart_item, created = CartItem.objects.get_or_create(
    cart=cart,
    product=product
)
```

এখন আমরা check করছি:

**এই Cart-এর মধ্যে এই Product আগে থেকেই আছে কিনা।**

দুইটি condition দেওয়া হয়েছে:

```python
cart=cart
product=product
```

অর্থাৎ:

```text
এই Cart
+
এই Product
```

এই combination-এর CartItem খুঁজবে।

---

# Example

ধরো:

```text
User = Rafiul
Product = Black Shirt
```

প্রথমবার Add to Cart:

```text
Rafiul's Cart
     ↓
Black Shirt
```

CartItem না থাকলে:

```text
CartItem created
quantity = 1
```

---

# 7. `created` আবার কেন?

```python
cart_item, created = CartItem.objects.get_or_create(...)
```

এখানে `created` বলবে CartItem নতুন তৈরি হয়েছে কিনা।

### প্রথমবার:

```text
CartItem নেই
     ↓
নতুন CartItem তৈরি
     ↓
created = True
```

### দ্বিতীয়বার:

```text
CartItem আগে থেকেই আছে
     ↓
Existing CartItem পাওয়া গেল
     ↓
created = False
```

---

# 8. Product আগে থেকেই থাকলে Quantity বাড়ানো

```python
if not created:
    cart_item.quantity += 1
    cart_item.save()
```

এটাই Add to Cart-এর সবচেয়ে গুরুত্বপূর্ণ অংশ।

`not created` মানে:

```text
created == False
```

অর্থাৎ CartItem আগে থেকেই ছিল।

---

## প্রথমবার Add to Cart

ধরো:

```text
Shirt
quantity = 1
```

প্রথমবার `get_or_create()` CartItem তৈরি করবে।

তখন:

```python
created = True
```

তাই:

```python
if not created:
```

condition false হবে।

Quantity বাড়বে না।

ফল:

```text
Shirt × 1
```

---

## দ্বিতীয়বার Add to Cart

আবার একই Shirt-এ Add to Cart করলে CartItem আগে থেকেই আছে।

তখন:

```python
created = False
```

তাই:

```python
if not created:
```

true হবে।

তারপর:

```python
cart_item.quantity += 1
```

যদি:

```text
quantity = 1
```

ছিল, তাহলে:

```text
quantity = 2
```

হবে।

তারপর:

```python
cart_item.save()
```

database-এ নতুন quantity save করবে।

---

# `+= 1` কী?

```python
cart_item.quantity += 1
```

এটা একই জিনিস:

```python
cart_item.quantity = cart_item.quantity + 1
```

উদাহরণ:

```text
1 → 2
2 → 3
3 → 4
4 → 5
```

---

# `cart_item.save()`

```python
cart_item.save()
```

এটা database-এ CartItem-এর পরিবর্তন save করে।

যেমন:

```text
আগে:
quantity = 1

     ↓

quantity += 1

     ↓

quantity = 2

     ↓

save()

     ↓

Database-এ quantity = 2
```

---

# 9. Success Message

```python
messages.success(
    request,
    f"{product.name} has been added to your cart."
)
```

Product Cart-এ successfully add হওয়ার পর user-কে success message দেখাবে।

ধরো product-এর নাম:

```text
Black Shirt
```

তাহলে message হবে:

```text
Black Shirt has been added to your cart.
```

এখানে:

```python
f"{product.name}"
```

ব্যবহার করে database-এর actual product name নেওয়া হচ্ছে।

---

# 10. Product Details Page-এ ফিরে যাওয়া

```python
return redirect("productDetails", id=product.id)
```

Add to Cart শেষ হওয়ার পর user-কে আবার Product Details page-এ পাঠানো হবে।

ধরো:

```text
Product ID = 7
```

তাহলে redirect হবে:

```text
/product/7/
```

অর্থাৎ:

```text
Add to Cart
     ↓
Cart update
     ↓
Success message
     ↓
Product Details page
```

---

# STEP 2.3 — URL তৈরি

এখন Django-কে বলতে হবে:

**এই URL-এ request এলে AddToCartView চালাবে।**

`urls.py`-তে:

```python
path(
    "product/<int:id>/add-to-cart/",
    views.AddToCartView.as_view(),
    name="add_to_cart"
),
```

---

# URL-এর প্রতিটি অংশ

## `"product/<int:id>/add-to-cart/"`

এটা URL pattern।

যেমন:

```text
/product/7/add-to-cart/
```

এখানে:

```text
<int:id>
```

মানে URL থেকে integer ID নেওয়া হবে।

তাই:

```text
/product/7/add-to-cart/
```

হলে:

```python
id = 7
```

---

# `views.AddToCartView.as_view()`

```python
views.AddToCartView.as_view()
```

আমরা `AddToCartView` class ব্যবহার করছি।

Django URL থেকে request এলে এই class-এর appropriate method চালাবে।

---

# `name="add_to_cart"`

```python
name="add_to_cart"
```

URL-এর একটি সহজ নাম।

এটার সুবিধা হলো template-এ পুরো URL manually লিখতে হবে না।

আমরা লিখতে পারি:

```django
{% url 'add_to_cart' product.id %}
```

Django নিজে URL তৈরি করবে।

---

# Product-related URLs

```python
path(
    "product/<int:id>/",
    views.ProductDetailsView.as_view(),
    name="productDetails"
),

path(
    "product/<int:id>/add-to-cart/",
    views.AddToCartView.as_view(),
    name="add_to_cart"
),
```

এখন:

```text
/product/7/
```

→ Product Details

আর:

```text
/product/7/add-to-cart/
```

→ Add to Cart

---

# STEP 2.4 — Product Details Button

আগে যদি button থাকে:

```html
<button
    class="bg-indigo-600 text-white px-8 py-3 rounded-lg
           hover:bg-indigo-700 w-fit">
    Add to Cart 🛒
</button>
```

এই button শুধু দেখতে button-এর মতো।

এটার কোনো URL/action নেই।

তাই এটাকে `<a>` link করা হয়েছে:

```html
<a
    href="{% url 'add_to_cart' product.id %}"
    class="bg-indigo-600 text-white px-8 py-3 rounded-lg
           hover:bg-indigo-700 w-fit inline-block
           transition duration-200">
    Add to Cart 🛒
</a>
```

---

# `{% url 'add_to_cart' product.id %}`

এটা Django Template Tag।

```django
{% url 'add_to_cart' product.id %}
```

Django:

1. `add_to_cart` নামে URL খুঁজবে
2. `product.id` থেকে ID নেবে
3. final URL তৈরি করবে

ধরো:

```text
product.id = 7
```

তাহলে:

```django
{% url 'add_to_cart' product.id %}
```

হয়ে যাবে:

```text
/product/7/add-to-cart/
```

---

# `href`

```html
href="{% url 'add_to_cart' product.id %}"
```

`href` বলে user click করলে browser কোন URL-এ যাবে।

তাই:

```text
Add to Cart
     ↓
href
     ↓
/product/7/add-to-cart/
```

---

# STEP 2.5 — পুরো Flow

ধরো Rafiul login করেছে এবং Product ID:

```text
7
```

Product Details:

```text
/product/7/
```

User click করল:

```text
Add to Cart 🛒
```

তারপর:

```text
/product/7/add-to-cart/
             ↓
      AddToCartView
             ↓
       id = 7
             ↓
   Product.objects.get(id=7)
             ↓
      Product পাওয়া গেল
             ↓
     request.user = Rafiul
             ↓
 Rafiul-এর Cart খুঁজবে
             ↓
      Cart আছে?
       ↙       ↘
     না          হ্যাঁ
     ↓            ↓
Create Cart    Existing Cart
       ↘        ↙
          ↓
   CartItem খুঁজবে
          ↓
 Product আগে আছে?
       ↙       ↘
     না          হ্যাঁ
     ↓            ↓
Create Item    quantity + 1
     ↓            ↓
quantity=1    quantity=2
       ↘        ↙
          ↓
    Success Message
          ↓
 Product Details
```

---

# প্রথমবার Add to Cart

Database conceptually:

```text
Cart

User = Rafiul
```

এবং:

```text
CartItem

Cart = Rafiul's Cart
Product = Shirt
Quantity = 1
```

---

# একই Product আবার Add করলে

নতুন CartItem তৈরি হবে না।

বরং:

```text
Existing CartItem
      ↓
quantity = 1
      ↓
quantity + 1
      ↓
quantity = 2
```

আবার click:

```text
2 → 3
```

---

# Different Product Add করলে

ধরো Rafiul প্রথমে Shirt add করল:

```text
Cart
 └── Shirt × 1
```

তারপর Pant add করল:

```text
Cart
 ├── Shirt × 1
 └── Pant × 1
```

অর্থাৎ একই Cart-এর মধ্যে multiple CartItem থাকবে।

---

# Login না থাকলে কী হবে?

আমরা ব্যবহার করেছি:

```python
class AddToCartView(LoginRequiredMixin, View):
```

তাই user login না করলে Add to Cart functionality access করতে পারবে না।

Django তাকে login page-এ redirect করবে।

`settings.py`-তে প্রয়োজন হলে:

```python
LOGIN_URL = "login"
```

রাখতে পারো।

---

# কেন `LoginRequiredMixin` এখন ব্যবহার করছি?

কারণ আমাদের বর্তমান Cart model:

```python
user = models.OneToOneField(
    User,
    ...
)
```

এর সাথে সরাসরি User যুক্ত।

অর্থাৎ Cart একজন নির্দিষ্ট logged-in User-এর।

তাই এখন:

```text
Guest
  ↓
No User
  ↓
No User Cart
```

এই কারণে login required।

পরের দিকে চাইলে আমরা **Guest Cart + Login Cart Merge** system তৈরি করতে পারব।

---

# Improvement — `get_object_or_404`

বর্তমানে:

```python
product = Product.objects.get(id=id)
```

ব্যবহার করছি।

এটা কাজ করবে, কিন্তু invalid ID দিলে exception হতে পারে।

আরও ভালো:

```python
from django.shortcuts import get_object_or_404
```

তারপর:

```python
product = get_object_or_404(Product, id=id)
```

এখন যদি Product ID database-এ না থাকে:

```text
/product/999999/
```

তাহলে Django সুন্দরভাবে:

```text
404 Page Not Found
```

দেবে।

---

# Important Concepts

## `get_or_create()`

```python
object, created = Model.objects.get_or_create(...)
```

অর্থ:

```text
আগে আছে?
   ↓
হ্যাঁ → existing object
না  → নতুন object তৈরি
```

---

## `created`

```text
True
```

→ নতুন object তৈরি হয়েছে।

```text
False
```

→ আগের object পাওয়া গেছে।

---

## `request.user`

বর্তমানে login করা user।

```python
request.user
```

---

## `product.id`

বর্তমান Product-এর database ID।

```python
product.id
```

---

## `quantity += 1`

Quantity এক বাড়ানো।

```text
1 → 2
2 → 3
3 → 4
```

---

## `redirect()`

এক view থেকে অন্য URL/page-এ পাঠায়।

```python
return redirect("productDetails", id=product.id)
```

---

# Complete `views.py` Concept

Relevant imports:

```python
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from .models import Customer, Product, Cart, CartItem
```

তারপর:

```python
class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, id):
        product = Product.objects.get(id=id)

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(
            request,
            f"{product.name} has been added to your cart."
        )

        return redirect("productDetails", id=product.id)
```

---

# Testing Checklist

এখন Cart Page বানানোর আগে শুধু এই functionality test করবে।

### Test 1 — Login

```text
Login
  ↓
Success
```

### Test 2 — Product Details

```text
Product Details
  ↓
Add to Cart
```

### Test 3 — প্রথমবার

Admin-এ গিয়ে দেখবে:

```text
Cart
User = Rafiul
```

এবং:

```text
CartItem
Product = Selected Product
Quantity = 1
```

### Test 4 — একই Product আবার Add

আবার Add to Cart করলে:

```text
Quantity = 2
```

হওয়া উচিত।

নতুন duplicate CartItem তৈরি হওয়া উচিত নয়।

### Test 5 — অন্য Product

অন্য Product Add করলে:

```text
Cart
 ├── Product A × 2
 └── Product B × 1
```

হওয়া উচিত।

---

# STEP 2 Final Concept

সবচেয়ে গুরুত্বপূর্ণভাবে মনে রাখবে:

```text
Add to Cart
     ↓
Product ID
     ↓
Find Product
     ↓
Find/Create User's Cart
     ↓
Find/Create CartItem
     ↓
Already exists?
   ↙          ↘
 No           Yes
 ↓             ↓
Create      Quantity + 1
 ↓             ↓
 1             2
       ↓
Save
       ↓
Success Message
       ↓
Product Details
```

**STEP 2-এর মূল শিক্ষা:**

`get_or_create()` দিয়ে আমরা নিশ্চিত করছি যে একই Cart-এর মধ্যে একই Product-এর জন্য duplicate CartItem তৈরি না হয়ে, পরেরবার quantity বাড়বে।
