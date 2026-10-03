# 🛒 Step 4 — Cart Page Template

## 🎯 Goal

`CartView` থেকে যে data পাঠাচ্ছি, সেটা `cart.html`-এ দেখানো।

View থেকে data:

```python
{
    "cart_items": cart_items,
    "total": total,
}
```

---

## 📁 Template File

তৈরি করো:

```text
templates/
└── shop/
    └── cart.html
```

---

## 🔗 Base Template Extend

`cart.html` শুরু হবে:

```django
{% extends "shop/base.html" %}
```

এর মাধ্যমে `base.html`-এর common layout ব্যবহার হবে।

---

## 📦 Content Block

Cart-এর পুরো UI থাকবে:

```django
{% block content %}

<!-- Cart UI -->

{% endblock %}
```

---

# 1️⃣ Cart Items দেখানো

View থেকে পাওয়া:

```python
cart_items
```

প্রতিটি item দেখানোর জন্য:

```django
{% for item in cart_items %}

    {{ item.product.name }}
    {{ item.quantity }}
    {{ item.subtotal }}

{% endfor %}
```

### এখানে

```django
item.product.name
```

→ Product-এর নাম

```django
item.quantity
```

→ কতটি product

```django
item.subtotal
```

→ Price × Quantity

---

# 2️⃣ Product Price

Discount থাকলে:

```django
item.product.discounted_price
```

ব্যবহার করবে।

না থাকলে:

```django
item.product.price
```

ব্যবহার করবে।

---

# 3️⃣ Product Image

Product-এর image:

```django
{{ item.product.image.url }}
```

---

# 4️⃣ Cart Total

View-তে calculate করা:

```python
total
```

Template-এ:

```django
{{ total }}
```

দিয়ে দেখানো হবে।

---

# 5️⃣ Empty Cart

যদি Cart-এ কোনো item না থাকে:

```django
{% if cart_items %}

    <!-- Cart Items -->

{% else %}

    <!-- Empty Cart -->

{% endif %}
```

অর্থাৎ:

```text
cart_items আছে
     ↓
Cart দেখাও

cart_items নেই
     ↓
"Your cart is empty"
```

---

# 6️⃣ Quantity + / − এবং Remove

Step 5-এ এই URLগুলো তৈরি করেছি:

```text
increase_cart
decrease_cart
remove_cart
```

`cart.html`-এ শুধু তাদের link/button বসাতে হবে।

### Quantity section:

```text
−   Quantity   +
```

* `−` → `decrease_cart`
* `+` → `increase_cart`

### Remove:

```text
Remove
```

→ `remove_cart`

HTML-এর exact code এখন এখানে repeat করার দরকার নেই।

---

# 🔄 Complete Flow

```text
Add to Cart
     ↓
CartView
     ↓
cart_items + total
     ↓
cart.html
     ↓
Product + Quantity + Subtotal + Total
     ↓
+ / − / Remove
     ↓
Django View
     ↓
Database Update
     ↓
Cart Page
```

---

# 🧠 মনে রাখবে

### View-এর কাজ

```python
CartView
```

→ Data prepare করবে।

### Template-এর কাজ

```text
cart.html
```

→ Data সুন্দরভাবে দেখাবে।

### Database-এর কাজ

```text
Cart
CartItem
Product
```

→ Actual information সংরক্ষণ করবে।

---

## ✅ Step 4 Summary

Step 4-এ মূলত:

```text
CartView
   ↓
cart_items
total
   ↓
cart.html
   ↓
Cart UI
```

তৈরি করেছি।

**Step 4 = Data দেখানো**

**Step 5 = Data পরিবর্তন করা (`+ / − / Remove`)**
