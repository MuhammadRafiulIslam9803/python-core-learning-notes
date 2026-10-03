# 🛒 Django E-commerce — Cart Page Setup (Step 3)

## 🎯 এই Step-এর Goal

এখন পর্যন্ত আমাদের flow ছিল:

```text
Product Details
      ↓
Add to Cart 🛒
      ↓
Cart তৈরি / CartItem তৈরি
      ↓
আবার Product Details Page
```

কারণ `AddToCartView`-এর শেষে ছিল:

```python
return redirect("productDetails", id=product.id)
```

এখন আমরা এটাকে পরিবর্তন করে **Cart Page**-এ নিয়ে যাব।

নতুন flow হবে:

```text
Product Details
      ↓
Add to Cart 🛒
      ↓
Cart তৈরি / CartItem তৈরি
      ↓
Cart Page
```

Cart Page-এ পরে আমরা দেখাব:

* Product Image
* Product Name
* Price
* Quantity
* Subtotal
* Total
* Quantity `+ / -`
* Remove
* Checkout

---

# 1️⃣ `views.py`-তে CartView তৈরি

`shop/views.py`-তে `CartView` যোগ করো:

```python
class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

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
            }
        )
```

---

# 2️⃣ Line-by-line Explanation

## `class CartView(LoginRequiredMixin, View):`

```python
class CartView(LoginRequiredMixin, View):
```

এখানে আমরা একটি **Class-Based View** তৈরি করছি।

### `LoginRequiredMixin`

Cart শুধুমাত্র logged-in user দেখতে পারবে।

যদি user login না করা থাকে:

```text
Cart → Login Page
```

আর login করা থাকলে:

```text
Cart → Cart Page
```

---

# 3️⃣ `get()` method

```python
def get(self, request):
```

User যখন browser থেকে Cart Page-এ যাবে:

```text
/cart/
```

তখন এই `get()` method execute হবে।

---

# 4️⃣ User-এর Cart খুঁজে বের করা

```python
cart, created = Cart.objects.get_or_create(
    user=request.user
)
```

এখানে Django দুইটা কাজ করতে পারে:

### যদি user-এর Cart আগে থেকেই থাকে

তাহলে সেই Cart নিয়ে আসবে।

```text
User
 ↓
Existing Cart
```

### যদি Cart না থাকে

তাহলে নতুন Cart তৈরি করবে।

```text
User
 ↓
No Cart
 ↓
Create Cart
```

`get_or_create()` দুইটি value return করে:

```python
cart
created
```

### `cart`

এটা হলো Cart object।

### `created`

এটা Boolean value:

```text
True  → নতুন Cart তৈরি হয়েছে
False → আগে থেকেই Cart ছিল
```

এই Step-এ `created` variable আমাদের আলাদাভাবে ব্যবহার করতে হচ্ছে না।

---

# 5️⃣ Cart-এর সব CartItem নেওয়া

```python
cart_items = cart.items.select_related("product")
```

এটা খুব গুরুত্বপূর্ণ।

আমাদের `CartItem` model-এ ছিল:

```python
cart = models.ForeignKey(
    Cart,
    on_delete=models.CASCADE,
    related_name="items"
)
```

তাই আমরা লিখতে পারি:

```python
cart.items
```

এর অর্থ:

```text
Cart
 ↓
CartItem 1
CartItem 2
CartItem 3
...
```

---

## `select_related("product")` কী?

আমাদের `CartItem`-এর মধ্যে Product-এর ForeignKey আছে:

```python
product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE
)
```

তাই:

```python
select_related("product")
```

বলছে:

> CartItem-এর সাথে সম্পর্কিত Product information-ও efficiently নিয়ে আসো।

এর ফলে Cart Page-এ আমরা সহজে ব্যবহার করতে পারব:

```python
item.product.name
item.product.price
item.product.image
```

---

# 6️⃣ Total শুরু করা

```python
total = 0
```

এখানে পুরো Cart-এর total price রাখার জন্য শুরুতে:

```text
total = 0
```

ধরা হয়েছে।

---

# 7️⃣ প্রতিটি CartItem-এর জন্য loop

```python
for item in cart_items:
```

ধরা যাক Cart-এ আছে:

```text
Shirt × 2
Pant  × 3
Shoes × 1
```

তাহলে loop একবার করে প্রতিটি CartItem-এর উপর কাজ করবে।

---

# 8️⃣ কোন Price ব্যবহার হবে?

```python
price = (
    item.product.discounted_price
    if item.product.discounted_price
    else item.product.price
)
```

এখানে আমরা প্রথমে দেখছি:

```python
item.product.discounted_price
```

আছে কি না।

### Discount থাকলে

ধরা যাক:

```text
Original Price = 1000
Discounted Price = 800
```

তাহলে:

```text
price = 800
```

### Discount না থাকলে

ধরা যাক:

```text
Original Price = 1000
Discounted Price = None
```

তাহলে:

```text
price = 1000
```

অর্থাৎ logic:

```text
Discounted Price আছে?
       ↓
     হ্যাঁ
       ↓
Discounted Price ব্যবহার

       অথবা

Discounted Price নেই
       ↓
Original Price ব্যবহার
```

---

# 9️⃣ Subtotal Calculate

```python
item.subtotal = price * item.quantity
```

প্রতিটি product-এর জন্য:

```text
Subtotal = Price × Quantity
```

### Example

ধরা যাক:

```text
Shirt
Price = 800
Quantity = 2
```

তাহলে:

```text
Subtotal = 800 × 2
         = 1600
```

এখানে:

```python
item.subtotal
```

এর মধ্যে `1600` রাখা হচ্ছে।

⚠️ `subtotal` আমাদের database model-এর field নয়।

এটা শুধু এই request-এর সময় Python object-এর মধ্যে temporary value হিসেবে রাখা হচ্ছে, যাতে template থেকে আমরা ব্যবহার করতে পারি:

```django
{{ item.subtotal }}
```

---

# 🔟 পুরো Cart-এর Total

```python
total += item.subtotal
```

প্রতিটি product-এর subtotal যোগ হয়ে:

```text
Cart Total
```

তৈরি হবে।

### Example

```text
Shirt:
800 × 2 = 1600

Pant:
500 × 3 = 1500

Shoes:
1200 × 1 = 1200
```

তাহলে:

```text
Total = 1600 + 1500 + 1200
      = 4300
```

---

# 1️⃣1️⃣ Template Render

```python
return render(
    request,
    "shop/cart.html",
    {
        "cart_items": cart_items,
        "total": total,
    }
)
```

এখানে Django বলছে:

> `shop/cart.html` template open করো এবং প্রয়োজনীয় data পাঠাও।

আমরা দুইটি data পাঠাচ্ছি:

```python
"cart_items": cart_items
```

এবং:

```python
"total": total
```

Template-এ এগুলো পাওয়া যাবে:

```django
{{ total }}
```

এবং:

```django
{% for item in cart_items %}
    ...
{% endfor %}
```

---

# 1️⃣2️⃣ `urls.py`-তে Cart URL

`shop/urls.py` অথবা যেখানে তোমার project URL রাখা আছে, সেখানে:

```python
path(
    "cart/",
    views.CartView.as_view(),
    name="cart",
),
```

এখানে:

### `"cart/"`

Browser URL:

```text
/cart/
```

### `views.CartView.as_view()`

এটা `CartView` class-কে URL-এর সাথে connect করছে।

### `name="cart"`

এই name দিয়ে আমরা Django-তে URL call করতে পারব:

```django
{% url 'cart' %}
```

অথবা Python থেকে:

```python
redirect("cart")
```

---

# 1️⃣3️⃣ AddToCartView-এর Redirect Change

আগে আমাদের ছিল:

```python
return redirect("productDetails", id=product.id)
```

এর অর্থ:

```text
Add to Cart
     ↓
Product Details Page
```

এখন এটাকে পরিবর্তন করব:

```python
return redirect("cart")
```

এখন flow:

```text
Add to Cart
     ↓
Cart Page
```

---

# 🔄 Final Flow

পুরো Step 3-এর flow:

```text
User
 ↓
Product Details
 ↓
Click "Add to Cart"
 ↓
AddToCartView
 ↓
Product খুঁজে বের করে
 ↓
User-এর Cart খুঁজে বের করে / তৈরি করে
 ↓
CartItem খুঁজে বের করে / তৈরি করে
 ↓
Quantity update করে
 ↓
redirect("cart")
 ↓
CartView
 ↓
Cart-এর সব CartItem নেয়
 ↓
Product information নেয়
 ↓
Price নির্ধারণ করে
 ↓
Subtotal calculate করে
 ↓
Total calculate করে
 ↓
shop/cart.html
```

---

# 🧮 Example

ধরা যাক user Cart-এ রেখেছে:

| Product | Price | Quantity | Subtotal |
| ------- | ----: | -------: | -------: |
| Shirt   |  ৳800 |        2 |    ৳1600 |
| Pant    |  ৳500 |        3 |    ৳1500 |
| Shoes   | ৳1200 |        1 |    ৳1200 |

তাহলে:

```text
Cart Total = ৳4300
```

View-এর ভিতরে:

```python
item.subtotal
```

হবে:

```text
Shirt → 1600
Pant  → 1500
Shoes → 1200
```

এবং:

```python
total
```

হবে:

```text
4300
```

---

# ⚠️ গুরুত্বপূর্ণ

এই Step-এ এখনো:

```text
cart.html
```

তৈরি করা হয়নি।

তাই Cart URL:

```text
/cart/
```

এ গেলে Django এমন error দিতে পারে:

```text
TemplateDoesNotExist
```

এটা স্বাভাবিক।

কারণ আমরা View এবং URL তৈরি করেছি, কিন্তু Template এখনো তৈরি করিনি।

পরের Step-এ আমরা তৈরি করব:

```text
shop/
└── templates/
    └── shop/
        └── cart.html
```

এবং সেখানে Tailwind দিয়ে professional Cart UI বানাব।

---

# 🧪 Testing Checklist

এই Step শেষ করার পর:

### 1. Server চালাও

```bash
python manage.py runserver
```

### 2. Login করো

```text
Login → Success
```

### 3. Product Details-এ যাও

```text
Product Details
```

### 4. Add to Cart চাপো

```text
Add to Cart 🛒
```

### 5. Expected flow

```text
Product Details
      ↓
Add to Cart
      ↓
Cart Page
```

### 6. Cart Page-এ error হলে

যদি:

```text
TemplateDoesNotExist: shop/cart.html
```

দেখায়, তাহলে চিন্তার কিছু নেই।

কারণ `cart.html` আমরা এখনো বানাইনি।

---

# 🧠 মনে রাখার মতো মূল বিষয়

### `get_or_create()`

```python
Cart.objects.get_or_create(
    user=request.user
)
```

মানে:

```text
আগে থাকলে → Get
না থাকলে → Create
```

### `select_related()`

```python
cart.items.select_related("product")
```

মানে:

```text
CartItem-এর সাথে সম্পর্কিত Product
information efficiently load করা।
```

### Subtotal

```python
item.subtotal = price * item.quantity
```

মানে:

```text
একটি Product-এর মোট দাম
```

### Total

```python
total += item.subtotal
```

মানে:

```text
সব Product-এর Subtotal যোগ করে
পুরো Cart-এর Total তৈরি করা।
```

### Redirect

```python
return redirect("cart")
```

মানে:

```text
Add to Cart শেষ
      ↓
Cart Page
```

---

# ✅ Step 3 Summary

এই Step-এ আমরা ৩টি গুরুত্বপূর্ণ কাজ করেছি:

```text
1. CartView তৈরি
       ↓
2. /cart/ URL তৈরি
       ↓
3. AddToCartView → Cart redirect
```

এর ফলে আমাদের e-commerce cart flow এখন:

```text
Product
   ↓
Product Details
   ↓
Add to Cart
   ↓
CartItem
   ↓
Cart Page
```

**পরবর্তী ধাপ:** `cart.html` তৈরি করে Product Image, Name, Price, Quantity, Subtotal এবং Total সুন্দরভাবে Tailwind UI-তে দেখানো।
