# 🛒 Cart Quantity `+ / −` এবং Remove — Step 5

## 🎯 Goal

এখন Cart Page-এ আমরা ৩টি operation তৈরি করছি:

```text
Cart Item
   │
   ├── Increase (+) → Quantity + 1
   │
   ├── Decrease (-) → Quantity - 1
   │
   └── Remove → CartItem Delete
```

এই কাজগুলো হবে **Django View + URL + Database** দিয়ে।

JavaScript এখন ব্যবহার করছি না।

---

# 1️⃣ IncreaseCartView

`views.py`-তে `CartView`-এর নিচে:

```python
class IncreaseCartView(LoginRequiredMixin, View):
    def get(self, request, id):
        cart_item = CartItem.objects.get(
            id=id,
            cart__user=request.user
        )

        cart_item.quantity += 1
        cart_item.save()

        return redirect("cart")
```

---

## Line by Line

### View তৈরি

```python
class IncreaseCartView(LoginRequiredMixin, View):
```

এটা CartItem-এর quantity বাড়ানোর জন্য একটি Class-Based View।

`LoginRequiredMixin` থাকার কারণে শুধুমাত্র logged-in user এই operation করতে পারবে।

---

### Product/CartItem-এর ID নেওয়া

```python
def get(self, request, id):
```

URL থেকে `id` আসবে।

উদাহরণ:

```text
/cart/15/increase/
```

এখানে:

```text
id = 15
```

অর্থাৎ CartItem-এর ID `15`।

---

### নির্দিষ্ট CartItem খোঁজা

```python
cart_item = CartItem.objects.get(
    id=id,
    cart__user=request.user
)
```

এখানে দুইটি condition আছে:

```text
id=id
```

মানে নির্দিষ্ট CartItem খুঁজবে।

এবং:

```text
cart__user=request.user
```

মানে CartItem-টি অবশ্যই বর্তমান logged-in user's Cart-এর হতে হবে।

---

# 🔐 `cart__user=request.user` কেন গুরুত্বপূর্ণ?

ধরা যাক:

```text
User A
 └── Cart
      └── CartItem ID = 15
```

User B যদি manually browser-এ লেখে:

```text
/cart/15/increase/
```

তাহলেও Django দেখবে:

```python
cart__user=request.user
```

CartItem 15 User B-এর Cart-এর নয়।

তাই User B সেটা modify করতে পারবে না।

এটা একটি গুরুত্বপূর্ণ **authorization/security check**।

---

# 2️⃣ Quantity Increase

```python
cart_item.quantity += 1
```

ধরা যাক:

```text
Quantity = 2
```

এই line-এর পরে:

```text
Quantity = 3
```

কারণ:

```text
2 + 1 = 3
```

---

# 3️⃣ Database Save

```python
cart_item.save()
```

Quantity memory-তে পরিবর্তন করার পর `save()` database-এ পরিবর্তনটি সংরক্ষণ করে।

Flow:

```text
Database
   ↓
quantity = 2
   ↓
Python
   ↓
quantity += 1
   ↓
quantity = 3
   ↓
save()
   ↓
Database
   ↓
quantity = 3
```

---

# 4️⃣ Cart Page-এ ফিরে যাওয়া

```python
return redirect("cart")
```

Quantity update হওয়ার পরে user আবার Cart Page-এ যাবে।

Flow:

```text
+ Button
   ↓
IncreaseCartView
   ↓
Quantity + 1
   ↓
save()
   ↓
redirect("cart")
   ↓
Cart Page
```

---

# 5️⃣ DecreaseCartView

```python
class DecreaseCartView(LoginRequiredMixin, View):
    def get(self, request, id):
        cart_item = CartItem.objects.get(
            id=id,
            cart__user=request.user
        )

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect("cart")
```

---

# 6️⃣ CartItem খোঁজা

এখানে একই security logic:

```python
cart_item = CartItem.objects.get(
    id=id,
    cart__user=request.user
)
```

অর্থাৎ:

```text
CartItem ID
    +
Current User
    ↓
নিজের CartItem
```

---

# 7️⃣ Quantity 1-এর বেশি হলে Decrease

```python
if cart_item.quantity > 1:
```

ধরা যাক:

```text
Quantity = 5
```

তাহলে:

```text
5 > 1
```

True হবে।

তখন:

```python
cart_item.quantity -= 1
cart_item.save()
```

হবে।

Result:

```text
5 → 4
```

---

# 8️⃣ Quantity কমানো

```python
cart_item.quantity -= 1
```

এটা equivalent:

```python
cart_item.quantity = cart_item.quantity - 1
```

উদাহরণ:

```text
Quantity = 3

3 - 1 = 2
```

Result:

```text
3 → 2
```

---

# 9️⃣ Quantity = 1 হলে কী হবে?

এখানে সবচেয়ে গুরুত্বপূর্ণ অংশ:

```python
else:
    cart_item.delete()
```

যদি:

```text
quantity = 1
```

তাহলে:

```python
quantity > 1
```

False হবে।

তখন CartItem delete হবে।

অর্থাৎ:

```text
Quantity = 1
       ↓
Minus (-)
       ↓
CartItem Delete
       ↓
Product Cart থেকে চলে যাবে
```

---

# 🔟 কেন Quantity 0 করছি না?

আমরা CartItem-এর quantity `0` রাখতে চাই না।

কারণ Cart-এ product থাকার অর্থ হলো অন্তত:

```text
quantity >= 1
```

তাই:

```text
1 → 0
```

না করে:

```text
1 → Delete CartItem
```

করছি।

এটা e-commerce cart-এর জন্য পরিষ্কার design।

---

# 1️⃣1️⃣ RemoveCartView

```python
class RemoveCartView(LoginRequiredMixin, View):
    def get(self, request, id):
        cart_item = CartItem.objects.get(
            id=id,
            cart__user=request.user
        )

        cart_item.delete()

        return redirect("cart")
```

এই View-এর কাজ শুধু CartItem delete করা।

---

## CartItem খোঁজা

```python
cart_item = CartItem.objects.get(
    id=id,
    cart__user=request.user
)
```

আবারও একই authorization check:

```text
CartItem অবশ্যই current user's Cart-এর হতে হবে।
```

---

## Delete

```python
cart_item.delete()
```

Database থেকে CartItem permanently delete হবে।

উদাহরণ:

```text
Cart

Shirt × 2
Pant  × 1
Shoes × 3
```

যদি Shirt-এর Remove চাপি:

```text
Cart

Pant  × 1
Shoes × 3
```

---

# 1️⃣2️⃣ URL Configuration

`urls.py`-তে `cart/` URL-এর নিচে এই ৩টি URL যোগ করতে হবে:

```python
path(
    "cart/<int:id>/increase/",
    views.IncreaseCartView.as_view(),
    name="increase_cart",
),

path(
    "cart/<int:id>/decrease/",
    views.DecreaseCartView.as_view(),
    name="decrease_cart",
),

path(
    "cart/<int:id>/remove/",
    views.RemoveCartView.as_view(),
    name="remove_cart",
),
```

---

# URL-এর অর্থ

## Increase

```text
/cart/15/increase/
```

মানে:

```text
CartItem ID = 15
       ↓
Quantity + 1
```

---

## Decrease

```text
/cart/15/decrease/
```

মানে:

```text
CartItem ID = 15
       ↓
Quantity - 1
```

---

## Remove

```text
/cart/15/remove/
```

মানে:

```text
CartItem ID = 15
       ↓
CartItem Delete
```

---

# 1️⃣3️⃣ HTML-এ কোথায় URL বসবে?

HTML code এখানে দেওয়ার প্রয়োজন নেই।

শুধু মনে রাখবে:

### `+` button

`cart.html`-এর **Quantity section-এর ভিতরে**:

```text
+ button
   ↓
increase_cart
```

### `−` button

একই **Quantity section-এর ভিতরে**:

```text
− button
   ↓
decrease_cart
```

### Remove

Cart item-এর **Subtotal section-এর নিচে**:

```text
Remove
   ↓
remove_cart
```

অর্থাৎ:

```text
cart.html

Cart Item
 ├── Product Info
 ├── Price
 ├── Quantity
 │    ├── − → decrease_cart
 │    ├── Quantity
 │    └── + → increase_cart
 │
 └── Subtotal
      └── Remove → remove_cart
```

---

# 🔄 পুরো Backend Flow

## Increase

```text
User clicks +
      ↓
/cart/<id>/increase/
      ↓
IncreaseCartView
      ↓
CartItem খুঁজে বের করা
      ↓
User-এর Cart কিনা check
      ↓
quantity += 1
      ↓
save()
      ↓
redirect("cart")
```

---

## Decrease

```text
User clicks −
      ↓
/cart/<id>/decrease/
      ↓
DecreaseCartView
      ↓
CartItem খুঁজে বের করা
      ↓
User-এর Cart কিনা check
      ↓
quantity > 1 ?
   ↓           ↓
 Yes           No
 ↓             ↓
-1            delete()
 ↓             ↓
save()         ↓
   └──────┬────┘
          ↓
   redirect("cart")
```

---

## Remove

```text
User clicks Remove
      ↓
/cart/<id>/remove/
      ↓
RemoveCartView
      ↓
CartItem খুঁজে বের করা
      ↓
User-এর Cart কিনা check
      ↓
delete()
      ↓
redirect("cart")
```

---

# 🔐 সবচেয়ে গুরুত্বপূর্ণ Security Concept

এই তিনটি View-তেই:

```python
cart__user=request.user
```

ব্যবহার করা হয়েছে।

এটা শুধু:

```text
CartItem আছে কি?
```

চেক করছে না।

এটা নিশ্চিত করছে:

```text
এই CartItem কি বর্তমানে login করা User-এর?
```

তাই:

```text
User A → নিজের CartItem modify/delete করতে পারবে ✅

User A → User B-এর CartItem modify/delete করতে পারবে না ❌
```

এটাই **ownership/authorization check**।

---

# 🧠 তিনটি View মনে রাখার সহজ নিয়ম

```text
IncreaseCartView
    → quantity += 1

DecreaseCartView
    → quantity -= 1
    → quantity = 1 হলে delete

RemoveCartView
    → সরাসরি delete
```

---

# 🧪 Testing

### Test 1 — Increase

```text
Quantity = 1
      ↓
+
      ↓
Quantity = 2
```

### Test 2 — Decrease

```text
Quantity = 3
      ↓
-
      ↓
Quantity = 2
```

### Test 3 — Quantity 1

```text
Quantity = 1
      ↓
-
      ↓
CartItem deleted
```

### Test 4 — Remove

```text
Quantity = 5
      ↓
Remove
      ↓
CartItem deleted
```

### Test 5 — Security

নিজের user-এর CartItem-এর ID নিয়ে কাজ করবে।

অন্য user-এর CartItem ID দিয়ে URL manually access করলে Django সেই CartItem পাবে না, কারণ:

```python
cart__user=request.user
```

condition match করবে না।

---

# ✅ Step 5 Summary

এই Step-এ আমরা database-এর CartItem-এর quantity এবং deletion control করার জন্য ৩টি View তৈরি করেছি:

```text
IncreaseCartView
      ↓
Quantity + 1

DecreaseCartView
      ↓
Quantity - 1
      ↓
Quantity 1 হলে Delete

RemoveCartView
      ↓
CartItem Delete
```

এবং প্রতিটি operation-এর আগে:

```python
cart__user=request.user
```

দিয়ে ownership/security check করেছি।

### পরবর্তী Cart Step

এখন Cart-এর basic functionality:

```text
Add
 ↓
View Cart
 ↓
Increase
 ↓
Decrease
 ↓
Remove
```

সম্পন্ন হয়েছে।

এরপর Cart-এর পরের অংশে **Navbar Cart Count / quantity count** এবং তারপর **Checkout/Order flow** নিয়ে এগোনো যাবে।
