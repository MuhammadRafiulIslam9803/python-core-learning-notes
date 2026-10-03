# Django Cart System — Step 1: Cart Foundation

## Roadmap

আমরা Cart System একবারে সব তৈরি করব না। ধাপে ধাপে করব।

1. Cart + CartItem Model
2. Migration
3. Product Details → Add to Cart
4. Cart Page-এ Product দেখানো
5. Quantity + / -
6. Remove Item
7. Navbar-এ Cart Count
8. Guest Cart + Login হলে Cart Merge
9. Checkout
10. Order + OrderItem
11. Payment / Order Status

---

# STEP 1 — Cart এবং CartItem Model

## আমাদের লক্ষ্য

একজন logged-in user-এর জন্য একটি shopping cart থাকবে।

তার Cart-এর মধ্যে এক বা একাধিক Product থাকতে পারবে।

ধরো:

```text
Rafiul
   │
   └── Cart
        │
        ├── Shirt × 2
        ├── Pant × 1
        └── Shoes × 1
```

এখানে:

* `Cart` = একজন user-এর পুরো shopping cart
* `CartItem` = Cart-এর ভিতরের একটি নির্দিষ্ট product
* `quantity` = ঐ product কতটি নেওয়া হয়েছে

---

# 1. Cart Model

`models.py`-তে `Product` model-এর নিচে:

```python
class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"
```

---

## Line by Line Explanation

### `class Cart(models.Model):`

```python
class Cart(models.Model):
```

এখানে আমরা Django-এর একটি নতুন Model তৈরি করছি যার নাম `Cart`।

`models.Model` inherit করার কারণে Django এই class-টিকে database table হিসেবে তৈরি করতে পারবে।

সহজভাবে:

```text
Python Class
     ↓
Django Model
     ↓
Database Table
```

---

## `user = models.OneToOneField(...)`

```python
user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name="cart"
)
```

এটা Cart এবং User-এর মধ্যে relationship তৈরি করছে।

### `User`

```python
User
```

এটা Django-এর built-in User model।

অর্থাৎ Cart কোন user-এর সেটা এখানে রাখা হবে।

উদাহরণ:

```text
User: Rafiul
Cart: Rafiul's Cart
```

---

## কেন `OneToOneField`?

```python
models.OneToOneField(...)
```

এর অর্থ:

**একজন User-এর সাথে একটি Cart থাকবে।**

ধরো:

```text
Rafiul → Cart 1
```

কিন্তু একই user-এর জন্য:

```text
Rafiul → Cart 1
Rafiul → Cart 2
```

এভাবে একাধিক Cart রাখা যাবে না।

আমাদের shopping cart-এর জন্য এটা দরকার, কারণ একজন logged-in user-এর একটি active cart থাকবে।

---

# `on_delete=models.CASCADE`

```python
on_delete=models.CASCADE
```

এর অর্থ হলো:

যদি কোনো User database থেকে delete করা হয়, তাহলে সেই User-এর Cart-ও automatically delete হবে।

উদাহরণ:

```text
User Rafiul
     ↓
Cart
     ↓
CartItem
```

User delete হলে তার Cart-এর relationship-ও আর থাকবে না।

---

# `related_name="cart"`

```python
related_name="cart"
```

এটা User থেকে তার Cart সহজে access করার জন্য ব্যবহার করা হয়েছে।

যেমন:

```python
user.cart
```

এতে ঐ user-এর Cart পাওয়া যাবে।

`related_name` না দিলে Django-এর default reverse relationship ব্যবহার করতে হতো।

আমাদের ক্ষেত্রে:

```python
user.cart
```

অনেক সহজ এবং readable।

---

# `created_at`

```python
created_at = models.DateTimeField(auto_now_add=True)
```

Cart প্রথম কখন তৈরি হয়েছে সেটা automatically save করবে।

`auto_now_add=True` মানে:

**Object প্রথম তৈরি হওয়ার সময় current date/time save হবে।**

উদাহরণ:

```text
Cart created:
2026-10-03 10:30
```

পরে Cart update হলেও `created_at` পরিবর্তন হবে না।

---

# `updated_at`

```python
updated_at = models.DateTimeField(auto_now=True)
```

Cart সর্বশেষ কখন update হয়েছে সেটা automatically save করবে।

`auto_now=True` মানে object save/update হওয়ার সময় সময়টি update হবে।

তাই:

```text
created_at → Cart প্রথম তৈরি হওয়ার সময়
updated_at → Cart সর্বশেষ update হওয়ার সময়
```

---

# `__str__()`

```python
def __str__(self):
    return f"{self.user.username}'s Cart"
```

এটা Django Admin এবং Python-এর বিভিন্ন জায়গায় Cart-কে readable name হিসেবে দেখানোর জন্য।

ধরো username:

```text
rafiul
```

তাহলে Admin-এ দেখা যাবে:

```text
rafiul's Cart
```

শুধু:

```text
Cart object (1)
```

দেখানোর পরিবর্তে meaningful নাম পাওয়া যাবে।

---

# 2. CartItem Model

এবার Cart-এর ভিতরে কোন কোন product আছে সেটা রাখার জন্য `CartItem` তৈরি করব।

```python
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_per_cart"
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
```

---

# `class CartItem(models.Model):`

```python
class CartItem(models.Model):
```

এটা Cart-এর ভিতরের individual product-এর information রাখবে।

উদাহরণ:

```text
Cart
 │
 ├── Shirt × 2
 ├── Pant × 1
 └── Shoes × 1
```

এখানে প্রত্যেকটি:

```text
Shirt × 2
Pant × 1
Shoes × 1
```

একেকটি `CartItem`।

---

# `cart = models.ForeignKey(...)`

```python
cart = models.ForeignKey(
    Cart,
    on_delete=models.CASCADE,
    related_name="items"
)
```

এটা CartItem এবং Cart-এর relationship তৈরি করছে।

এখানে `ForeignKey` ব্যবহার করা হয়েছে কারণ:

**একটি Cart-এর মধ্যে অনেক CartItem থাকতে পারে।**

অর্থাৎ:

```text
Cart
 │
 ├── CartItem 1
 ├── CartItem 2
 ├── CartItem 3
 └── CartItem 4
```

এটা হলো:

**One-to-Many relationship**

একটি Cart → অনেক CartItem

---

# `related_name="items"`

```python
related_name="items"
```

এটার কারণে Cart থেকে তার সব CartItem সহজে পাওয়া যাবে।

যেমন:

```python
cart.items.all()
```

এতে ঐ Cart-এর সব CartItem পাওয়া যাবে।

---

# `product = models.ForeignKey(...)`

```python
product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE
)
```

এটা বলে:

**এই CartItem কোন Product-এর সেটা এখানে থাকবে।**

যেমন:

```text
CartItem
   ↓
Product = Black Shirt
```

আরেকটি:

```text
CartItem
   ↓
Product = Blue Pant
```

---

# কেন এখানে ForeignKey?

একটি Product অনেক user's Cart-এ থাকতে পারে।

উদাহরণ:

```text
Black Shirt
    │
    ├── Rafiul's Cart
    ├── Adnan's Cart
    └── Riham's Cart
```

তাই Product-এর সাথে অনেক CartItem তৈরি হতে পারে।

---

# `quantity`

```python
quantity = models.PositiveIntegerField(default=1)
```

এটা বলে user ঐ product কতটি নিতে চায়।

উদাহরণ:

```text
Shirt → quantity = 1
```

User আবার `+` চাপলে:

```text
Shirt → quantity = 2
```

আবার:

```text
Shirt → quantity = 3
```

### `PositiveIntegerField`

এখানে positive integer ব্যবহার করা হয়েছে।

অর্থাৎ:

```text
1
2
3
4
...
```

রাখা যাবে।

Negative quantity যেমন:

```text
-1
-5
```

রাখা যাবে না।

### `default=1`

নতুন CartItem তৈরি করার সময় quantity না দিলে default হিসেবে:

```text
quantity = 1
```

হবে।

---

# `created_at`

```python
created_at = models.DateTimeField(auto_now_add=True)
```

CartItem কখন প্রথম তৈরি হয়েছে সেটা রাখবে।

---

# `updated_at`

```python
updated_at = models.DateTimeField(auto_now=True)
```

CartItem সর্বশেষ কখন update হয়েছে সেটা রাখবে।

যেমন quantity পরিবর্তন করলে `updated_at` update হবে।

---

# UniqueConstraint

এটা Cart System-এর খুব গুরুত্বপূর্ণ অংশ।

```python
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=["cart", "product"],
            name="unique_product_per_cart"
        )
    ]
```

এর উদ্দেশ্য:

**একই Cart-এর মধ্যে একই Product-এর duplicate CartItem তৈরি হতে না দেওয়া।**

---

## Constraint ছাড়া কী হতে পারত?

ধরো:

```text
Rafiul's Cart

CartItem 1:
Product = Shirt
Quantity = 1

CartItem 2:
Product = Shirt
Quantity = 1
```

এখন একই Shirt দুইবার আলাদা CartItem হয়ে গেল।

আমরা সাধারণত এটা চাই না।

আমরা চাই:

```text
Rafiul's Cart

CartItem:
Product = Shirt
Quantity = 2
```

---

# `fields=["cart", "product"]`

```python
fields=["cart", "product"]
```

এর অর্থ:

একটি Cart-এর মধ্যে একই Product দ্বিতীয়বার আলাদা CartItem হিসেবে রাখা যাবে না।

কিন্তু অন্য user একই Product নিজের Cart-এ রাখতে পারবে।

উদাহরণ:

```text
Rafiul's Cart
    → Shirt × 2

Adnan's Cart
    → Shirt × 1
```

এটা valid।

কারণ Cart আলাদা।

কিন্তু:

```text
Rafiul's Cart
    → Shirt × 1
Rafiul's Cart
    → Shirt × 1
```

এটা constraint অনুযায়ী duplicate হবে।

---

# `name="unique_product_per_cart"`

```python
name="unique_product_per_cart"
```

এটা database constraint-এর একটি unique name।

এর মাধ্যমে Django/database এই constraint-টিকে identify করতে পারে।

---

# CartItem-এর `__str__()`

```python
def __str__(self):
    return f"{self.product.name} - {self.quantity}"
```

ধরো:

```text
Product name = Black Shirt
quantity = 2
```

তাহলে Django Admin-এ readableভাবে দেখাবে:

```text
Black Shirt - 2
```

এর বদলে:

```text
CartItem object (1)
```

দেখাবে না।

---

# পুরো Relationship একসাথে

আমাদের database relationship এখন এমন:

```text
User
 │
 │ OneToOne
 ↓
Cart
 │
 │ OneToMany
 ↓
CartItem
 │
 │ ForeignKey
 ↓
Product
```

আর বাস্তবে:

```text
User: Rafiul
       │
       ↓
    Cart
       │
       ├───────────────┐
       ↓               ↓
   CartItem 1      CartItem 2
       │               │
       ↓               ↓
   Shirt × 2       Pant × 1
```

---

# Product কেন সরাসরি Cart-এর সাথে রাখা হয়নি?

আমরা এভাবে করিনি:

```text
Cart
 ├── Product
 ├── Product
 └── Product
```

বরং:

```text
Cart
 ↓
CartItem
 ↓
Product
```

কারণ `CartItem`-এর মধ্যে আমরা extra information রাখতে পারি।

যেমন:

```text
Product
Quantity
Price at the time
Added time
Discount
```

ভবিষ্যতে Order System বানানোর সময় এই structure অনেক useful হবে।

---

# Complete Code

`models.py`-তে Product model-এর পরে:

```python
class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_per_cart"
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
```

---

# STEP 2 — Migration

Model তৈরি করার পর Django-কে database structure update করতে বলতে হবে।

প্রথমে:

```bash
python manage.py makemigrations
```

### `makemigrations` কী করে?

Django তোমার `models.py` দেখে বুঝবে:

```text
নতুন Cart model তৈরি হয়েছে
নতুন CartItem model তৈরি হয়েছে
```

তারপর migration file তৈরি করবে।

---

এরপর:

```bash
python manage.py migrate
```

### `migrate` কী করে?

Migration-এর instructions database-এ apply করবে।

ফলে database-এ নতুন table তৈরি হবে।

সহজভাবে:

```text
models.py
    ↓
makemigrations
    ↓
Migration file
    ↓
migrate
    ↓
Database tables
```

---

# Expected Database Structure

Migration সফল হলে ধারণাগতভাবে database-এ থাকবে:

```text
Cart
--------------------------------
id
user_id
created_at
updated_at
```

এবং:

```text
CartItem
--------------------------------
id
cart_id
product_id
quantity
created_at
updated_at
```

এখানে `cart_id` Cart-এর সাথে এবং `product_id` Product-এর সাথে relationship রাখবে।

---

# Important Concept Summary

### Cart

একজন user-এর shopping cart।

```text
User → Cart
```

Relationship:

```text
OneToOne
```

---

### CartItem

Cart-এর ভিতরে থাকা একটি product এবং তার quantity।

```text
Cart → CartItem
```

Relationship:

```text
OneToMany
```

---

### Product

তোমার existing Product model।

```text
CartItem → Product
```

Relationship:

```text
ForeignKey
```

---

### Quantity

একই product কতটি নেওয়া হয়েছে।

```text
Shirt × 2
```

---

### UniqueConstraint

একই Cart-এর মধ্যে একই Product-এর duplicate CartItem আটকায়।

```text
Same Cart + Same Product
        ↓
      Unique
```

---

# STEP 1 Complete Checklist

* [ ] `Cart` model তৈরি
* [ ] `Cart`-এর সাথে `User` OneToOne
* [ ] `CartItem` model তৈরি
* [ ] `CartItem`-এর সাথে `Cart` ForeignKey
* [ ] `CartItem`-এর সাথে `Product` ForeignKey
* [ ] `quantity` field
* [ ] `created_at`
* [ ] `updated_at`
* [ ] `UniqueConstraint`
* [ ] `makemigrations`
* [ ] `migrate`

**এই ধাপের মূল ধারণা:**

```text
একজন User
    ↓
একটি Cart
    ↓
অনেক CartItem
    ↓
প্রতিটি CartItem একটি Product + Quantity
```

পরের ধাপে আমরা এই foundation-এর উপর **Product Details page-এর "Add to Cart" functionality** তৈরি করব।
