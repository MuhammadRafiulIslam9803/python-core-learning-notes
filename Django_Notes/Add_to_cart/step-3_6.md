# Django Cart System — Step 6: Navbar Cart Count

## আমাদের লক্ষ্য

এখন পর্যন্ত আমরা Cart এবং CartItem তৈরি করেছি।

এখন চাই navbar-এর যেকোনো page থেকে user-এর Cart-এর quantity দেখা যাবে।

Navbar:

```text
Home   Products   🛒 Cart (3)   Profile   Logout
```

যদি Cart-এ থাকে:

```text
Shirt × 2
Pant × 3
Shoes × 1
```

তাহলে:

```text
🛒 Cart 6
```

দেখাবে।

---

# কেন Context Processor ব্যবহার করছি?

ধরো আমাদের website-এর অনেকগুলো template আছে:

```text
home.html
productDetails.html
cart.html
profile.html
about.html
```

Navbar যদি `base.html`-এ থাকে, তাহলে প্রতিটি view থেকে আলাদাভাবে:

```python
return render(
    request,
    "shop/home.html",
    {"cart_count": cart_count}
)
```

এভাবে `cart_count` পাঠানো ঝামেলার হবে।

আমরা চাই:

**সব template যেন automatically `cart_count` পায়।**

এই কাজের জন্য Django-এর **Context Processor** ব্যবহার করছি।

---

# STEP 6.1 — `context_processors.py` তৈরি

`shop` app-এর ভিতরে নতুন file:

```text
shop/
├── models.py
├── views.py
├── urls.py
├── forms.py
└── context_processors.py
```

`context_processors.py`:

```python
from .models import Cart


def cart_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()

        if cart:
            count = sum(
                item.quantity
                for item in cart.items.all()
            )

            return {
                "cart_count": count
            }

    return {
        "cart_count": 0
    }
```

---

# Line by Line Explanation

## 1. Cart import

```python
from .models import Cart
```

আমরা Cart model ব্যবহার করব।

তাই `models.py` থেকে `Cart` import করছি।

---

# 2. Function তৈরি

```python
def cart_count(request):
```

এটা একটি Context Processor function।

Django প্রতিবার template render করার সময় এই function চালাতে পারবে।

`request` argument-এর মাধ্যমে আমরা জানতে পারব:

**বর্তমানে কে website ব্যবহার করছে?**

---

# 3. User login করেছে কিনা check

```python
if request.user.is_authenticated:
```

এখানে check হচ্ছে:

```text
User login করেছে?
       ↓
    Yes / No
```

### যদি login করা থাকে

```text
request.user.is_authenticated
        ↓
       True
```

তাহলে Cart খুঁজবে।

### যদি login করা না থাকে

```text
request.user.is_authenticated
        ↓
       False
```

তাহলে Cart খোঁজার দরকার নেই।

কারণ আমাদের বর্তমান Cart system user-based।

---

# 4. User-এর Cart খোঁজা

```python
cart = Cart.objects.filter(
    user=request.user
).first()
```

এখানে আমরা current logged-in user-এর Cart খুঁজছি।

```python
request.user
```

মানে বর্তমানে login করা user।

ধরো:

```text
Logged-in user = Rafiul
```

তাহলে:

```python
user=request.user
```

মানে:

```text
user = Rafiul
```

---

# কেন `.filter()` ব্যবহার করছি?

```python
Cart.objects.filter(user=request.user)
```

এটা matching Cart-এর QuerySet দেয়।

আমাদের একজন User-এর একটি Cart থাকার কথা, কারণ Cart model-এ:

```python
user = models.OneToOneField(...)
```

আছে।

তারপর:

```python
.first()
```

দিয়ে প্রথম Cart object নেওয়া হচ্ছে।

ফলে:

```python
cart
```

এর মধ্যে user's Cart থাকবে।

---

# 5. Cart আছে কিনা check

```python
if cart:
```

এখানে check করছি:

```text
User-এর Cart পাওয়া গেছে?
       ↓
   Yes / No
```

যদি Cart থাকে:

```text
if cart:
    ...
```

এর ভিতরের code চলবে।

যদি Cart না থাকে, সরাসরি নিচের অংশে যাবে:

```python
return {
    "cart_count": 0
}
```

---

# 6. Cart-এর সব CartItem নেওয়া

```python
cart.items.all()
```

এটা বুঝতে `related_name` মনে করতে হবে।

আমাদের CartItem model-এ ছিল:

```python
cart = models.ForeignKey(
    Cart,
    on_delete=models.CASCADE,
    related_name="items"
)
```

এখানে:

```python
related_name="items"
```

দেওয়ার কারণে আমরা Cart থেকে লিখতে পারি:

```python
cart.items.all()
```

মানে:

**এই Cart-এর সব CartItem আমাকে দাও।**

উদাহরণ:

```text
Rafiul's Cart
     │
     ├── Shirt × 2
     ├── Pant × 3
     └── Shoes × 1
```

তাহলে:

```python
cart.items.all()
```

এই তিনটি CartItem return করবে।

---

# 7. `sum()` দিয়ে Total Quantity

```python
count = sum(
    item.quantity
    for item in cart.items.all()
)
```

এটাই Cart Count-এর মূল logic।

ধরো:

```text
Shirt → quantity = 2
Pant  → quantity = 3
Shoes → quantity = 1
```

তাহলে:

```text
2 + 3 + 1
```

ফল:

```text
6
```

তাই:

```python
count = 6
```

---

# `for item in cart.items.all()` কী করছে?

এটা Cart-এর প্রতিটি CartItem একে একে নিচ্ছে।

ধরো:

```text
CartItem 1 → Shirt → quantity 2
CartItem 2 → Pant  → quantity 3
CartItem 3 → Shoes → quantity 1
```

তখন:

```python
item.quantity
```

একবার করে:

```text
2
3
1
```

পাবে।

তারপর `sum()` সব যোগ করবে:

```text
2 + 3 + 1 = 6
```

---

# 8. Context-এ `cart_count` পাঠানো

```python
return {
    "cart_count": count
}
```

এখন Django template-এর মধ্যে:

```django
{{ cart_count }}
```

ব্যবহার করা যাবে।

যদি:

```python
count = 6
```

হয়, তাহলে:

```django
{{ cart_count }}
```

দেখাবে:

```text
6
```

---

# 9. Cart না থাকলে

যদি user login করা না থাকে অথবা Cart না থাকে:

```python
return {
    "cart_count": 0
}
```

তাহলে template-এ:

```django
{{ cart_count }}
```

এর value হবে:

```text
0
```

---

# STEP 6.2 — `settings.py`-তে Context Processor যোগ

এখন শুধু function তৈরি করলেই হবে না।

Django-কে বলতে হবে:

**এই Context Processor ব্যবহার করো।**

`settings.py` → `TEMPLATES` → `context_processors`:

```python
"OPTIONS": {
    "context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",

        "shop.context_processors.cart_count",
    ],
},
```

---

# `"shop.context_processors.cart_count"`

এটা বুঝি।

```text
shop
  ↓
context_processors
  ↓
cart_count
```

অর্থাৎ:

```text
shop app
   ↓
context_processors.py
   ↓
cart_count function
```

যদি তোমার app-এর নাম `shop` না হয়, তাহলে actual app name ব্যবহার করবে।

উদাহরণ:

```text
myshop.context_processors.cart_count
```

---

# Context Processor-এর পুরো Flow

```text
Browser Request
      ↓
Django
      ↓
Context Processor
      ↓
cart_count(request)
      ↓
Current User
      ↓
User-এর Cart
      ↓
Cart-এর CartItems
      ↓
Quantity যোগ
      ↓
cart_count
      ↓
সব Template-এ available
```

---

# STEP 6.3 — Navbar-এ Cart দেখানো

`base.html`-এ যেখানে Cart link রাখতে চাও:

```html
<a
    href="{% url 'cart' %}"
    class="relative flex items-center gap-1
           text-gray-700 hover:text-indigo-600">

    🛒 Cart

    {% if cart_count > 0 %}
        <span
            class="bg-indigo-600 text-white
                   text-xs font-bold
                   rounded-full px-2 py-0.5">
            {{ cart_count }}
        </span>
    {% endif %}

</a>
```

---

# `href="{% url 'cart' %}"`

```html
href="{% url 'cart' %}"
```

এটা Cart page-এর URL তৈরি করবে।

এখানে:

```text
cart
```

হলো URL-এর `name`।

তোমার `urls.py`-তে Cart page-এর URL-এ অবশ্যই:

```python
name="cart"
```

থাকতে হবে।

---

# `🛒 Cart`

```html
🛒 Cart
```

এটা navbar-এ Cart text এবং icon দেখাবে।

---

# `{% if cart_count > 0 %}`

```django
{% if cart_count > 0 %}
```

এখানে check হচ্ছে:

```text
Cart count > 0 ?
```

### যদি 0 হয়

```text
🛒 Cart
```

শুধু Cart দেখাবে।

### যদি 0-এর বেশি হয়

```text
🛒 Cart 3
```

count দেখাবে।

---

# `<span>`

```html
<span
    class="bg-indigo-600 text-white
           text-xs font-bold
           rounded-full px-2 py-0.5">
    {{ cart_count }}
</span>
```

এটা count-এর জন্য ছোট badge তৈরি করছে।

যেমন:

```text
🛒 Cart 6
       ↑
     Badge
```

---

# STEP 6.4 — Example

ধরো Rafiul-এর Cart:

```text
Product       Quantity
----------------------
Shirt            2
Pant             3
Shoes            1
```

Context Processor:

```python
count = sum(
    item.quantity
    for item in cart.items.all()
)
```

হিসাব:

```text
2 + 3 + 1 = 6
```

তাই:

```python
cart_count = 6
```

Navbar:

```text
🛒 Cart 6
```

---

# Quantity vs Product Count

এখানে খুব গুরুত্বপূর্ণ একটি বিষয় আছে।

আমরা এখন **total quantity** count করছি।

ধরো:

```text
Shirt × 2
Pant × 3
Shoes × 1
```

আমাদের count:

```text
2 + 3 + 1 = 6
```

তাই:

```text
🛒 Cart 6
```

---

## যদি Product Type Count চাই

যদি শুধু কত ধরনের Product আছে সেটা চাই:

```text
Shirt
Pant
Shoes
```

তাহলে:

```text
3
```

হবে।

সেক্ষেত্রে:

```python
cart.items.count()
```

ব্যবহার করা যায়।

তখন:

```text
Shirt × 2
Pant × 3
Shoes × 1

Cart = 3
```

কারণ CartItem আছে ৩টি।

---

# আমরা এখন কোনটা ব্যবহার করছি?

আমরা ব্যবহার করছি:

```python
sum(
    item.quantity
    for item in cart.items.all()
)
```

অর্থাৎ:

**Total Product Quantity**

উদাহরণ:

```text
Shirt × 2
Pant × 3
Shoes × 1

Cart (6)
```

---

# কেন Context Processor এখানে ভালো?

Navbar প্রায় সব page-এ থাকে।

যেমন:

```text
Home
Products
Product Details
Profile
Cart
Checkout
```

প্রতিটি view-তে আলাদাভাবে:

```python
cart_count = ...
```

লিখতে হলে code duplicate হতো।

Context Processor ব্যবহার করলে:

```text
একবার logic
     ↓
সব template
```

তাই এটা এই ধরনের global navbar data-এর জন্য useful।

---

# Complete `context_processors.py`

```python
from .models import Cart


def cart_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()

        if cart:
            count = sum(
                item.quantity
                for item in cart.items.all()
            )

            return {
                "cart_count": count
            }

    return {
        "cart_count": 0
    }
```

---

# Complete `settings.py` অংশ

```python
"OPTIONS": {
    "context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "shop.context_processors.cart_count",
    ],
},
```

---

# Complete Navbar অংশ

```html
<a
    href="{% url 'cart' %}"
    class="relative flex items-center gap-1
           text-gray-700 hover:text-indigo-600">

    🛒 Cart

    {% if cart_count > 0 %}
        <span
            class="bg-indigo-600 text-white
                   text-xs font-bold
                   rounded-full px-2 py-0.5">
            {{ cart_count }}
        </span>
    {% endif %}

</a>
```

---

# পুরো System-এর Flow

এখন পর্যন্ত আমাদের Cart System:

```text
                     USER
                       │
                       ↓
                     CART
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
        CART ITEM 1         CART ITEM 2
             ↓                   ↓
          Shirt                Pant
        quantity 2          quantity 3
             │                   │
             └─────────┬─────────┘
                       ↓
                Context Processor
                       ↓
               quantity যোগ করে
                       ↓
                  cart_count
                       ↓
                    Navbar
                       ↓
                 🛒 Cart 5
```

---

# Important Concepts

## Context Processor

Template-এ globally/common data available করার Django mechanism।

```text
Context Processor
       ↓
All Templates
```

---

## `request.user`

বর্তমানে login করা user:

```python
request.user
```

---

## `is_authenticated`

User login করেছে কিনা check:

```python
request.user.is_authenticated
```

---

## `related_name="items"`

CartItem model-এ:

```python
related_name="items"
```

থাকার কারণে:

```python
cart.items.all()
```

দিয়ে Cart-এর সব CartItem পাওয়া যায়।

---

## `sum()`

সব quantity যোগ করে:

```python
sum(
    item.quantity
    for item in cart.items.all()
)
```

---

## `cart_count`

এটা আমাদের template-এর variable:

```django
{{ cart_count }}
```

---

# Testing Checklist

### Test 1 — User login না করলে

```text
🛒 Cart
```

count দেখানোর দরকার নেই।

### Test 2 — Empty Cart

```text
🛒 Cart
```

### Test 3 — One Product

```text
Shirt × 1

🛒 Cart 1
```

### Test 4 — Same Product দুইবার

```text
Shirt × 2

🛒 Cart 2
```

### Test 5 — Multiple Products

```text
Shirt × 2
Pant × 3
Shoes × 1
```

Navbar:

```text
🛒 Cart 6
```

---

# STEP 6-এর মূল শিক্ষা

সবচেয়ে গুরুত্বপূর্ণ flow:

```text
Login User
    ↓
Find User's Cart
    ↓
Find CartItems
    ↓
Get quantity of each item
    ↓
sum()
    ↓
cart_count
    ↓
Context Processor
    ↓
All Templates
    ↓
Navbar
    ↓
🛒 Cart 6
```

**মূল কথা:** `context_processors.py` ব্যবহার করার কারণে প্রতিটি view থেকে আলাদাভাবে `cart_count` পাঠানোর প্রয়োজন হচ্ছে না। Django request-এর সময় এই data template context-এ automatically যোগ করে দিচ্ছে।
