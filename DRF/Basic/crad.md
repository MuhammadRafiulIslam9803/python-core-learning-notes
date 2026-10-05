# Django REST API — studentData CRUD Notes

## Complete Code

```python
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def studentData(request):

    # =========================
    # GET → সব Student নেওয়া
    # =========================

    if request.method == 'GET':

        students = Student.objects.all()

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)


    # =========================
    # POST → নতুন Student তৈরি
    # =========================

    elif request.method == 'POST':

        serializer = StudentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


    # =========================
    # PUT → পুরো Student Update
    # =========================

    elif request.method == 'PUT':

        # Request থেকে Student-এর ID নিলাম
        student_id = request.data.get('id')

        # ওই ID দিয়ে Database থেকে Student বের করলাম
        object = Student.objects.get(
            id=student_id
        )

        # পুরোনো object + নতুন data
        serializer = StudentSerializer(
            object,
            data=request.data
        )

        if serializer.is_valid():

            # Database-এ update করলাম
            serializer.save()

            return Response(
                serializer.data,
                status=200
            )

        return Response(
            serializer.errors,
            status=400
        )


    # =========================
    # PATCH → Student-এর কিছু অংশ Update
    # =========================

    elif request.method == 'PATCH':

        # Request থেকে Student-এর ID নিলাম
        student_id = request.data.get('id')

        # ওই ID দিয়ে Database থেকে Student বের করলাম
        object = Student.objects.get(
            id=student_id
        )

        # partial=True → সব field দেওয়া লাগবে না
        serializer = StudentSerializer(
            object,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            # Database-এ update করলাম
            serializer.save()

            return Response(
                serializer.data,
                status=200
            )

        return Response(
            serializer.errors,
            status=400
        )


    # =========================
    # DELETE → Student Delete
    # =========================

    elif request.method == 'DELETE':

        # Request থেকে Student-এর ID নিলাম
        student_id = request.data.get('id')

        # ওই ID দিয়ে Database থেকে Student বের করলাম
        object = Student.objects.get(
            id=student_id
        )

        # Student-কে Database থেকে delete করলাম
        object.delete()

        # 204 → Successfully deleted, কিন্তু return করার data নেই
        return Response(status=204)
```

---

# 1. GET — সব Student নেওয়া

```python
if request.method == 'GET':

    students = Student.objects.all()

    serializer = StudentSerializer(
        students,
        many=True
    )

    return Response(serializer.data)
```

### সহজভাবে

> এখানে আমরা **request থেকে কিছু নিচ্ছি না**।

প্রথমে:

```python
students = Student.objects.all()
```

Database থেকে **সব Student** নিলাম এবং `students`-এর মধ্যে রাখলাম।

তারপর:

```python
serializer = StudentSerializer(
    students,
    many=True
)
```

Student object-গুলোকে **Serializer-এর মাধ্যমে JSON-এর উপযোগী data** বানালাম।

এখানে:

```python
many=True
```

দিয়েছি কারণ আমরা **একজন Student না, অনেক Student** নিয়ে কাজ করছি।

শেষে:

```python
return Response(serializer.data)
```

Serializer-এর data response হিসেবে পাঠালাম।

### GET Flow

```text
Database
   ↓
সব Student নেওয়া
   ↓
Serializer
   ↓
JSON Data
   ↓
Response
```

---

# 2. POST — নতুন Student তৈরি করা

```python
elif request.method == 'POST':

    serializer = StudentSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=201
        )

    return Response(
        serializer.errors,
        status=400
    )
```

### সহজভাবে

প্রথমে:

```python
request.data
```

এর মাধ্যমে **request থেকে নতুন Student-এর data নিলাম**।

তারপর:

```python
serializer = StudentSerializer(
    data=request.data
)
```

Request থেকে আসা data-কে Serializer-এর মধ্যে রাখলাম।

এরপর:

```python
serializer.is_valid()
```

দিয়ে check করলাম **data ঠিক আছে কিনা**।

যদি ঠিক থাকে:

```python
serializer.save()
```

দিয়ে **Database-এ নতুন Student তৈরি করে save করলাম**।

তারপর:

```python
return Response(
    serializer.data,
    status=201
)
```

নতুন Student-এর data return করলাম।

`201` মানে:

> **Successfully Created**

আর যদি data ভুল হয়:

```python
return Response(
    serializer.errors,
    status=400
)
```

ভুলগুলো return করলাম।

`400` মানে:

> **Bad Request / Request-এর data-তে সমস্যা আছে**

### POST Flow

```text
Request
   ↓
request.data
   ↓
Serializer
   ↓
is_valid()
   ↓
Valid?
 ┌───────┴───────┐
Yes              No
 ↓                 ↓
save()          errors
 ↓                 ↓
201             400
```

---

# 3. PUT — পুরো Student Update

```python
elif request.method == 'PUT':

    student_id = request.data.get('id')

    object = Student.objects.get(
        id=student_id
    )

    serializer = StudentSerializer(
        object,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=200
        )

    return Response(
        serializer.errors,
        status=400
    )
```

### Step 1 — Request থেকে ID নেওয়া

```python
student_id = request.data.get('id')
```

Request থেকে Student-এর `id` নিলাম এবং `student_id`-এর মধ্যে রাখলাম।

---

### Step 2 — ID দিয়ে Student বের করা

```python
object = Student.objects.get(
    id=student_id
)
```

Database-এর মধ্যে ওই `id`-র সাথে যে Student মিলে, **সেই Student object-টা `object`-এর মধ্যে রাখলাম**।

---

### Step 3 — পুরোনো Object + নতুন Data Serializer-এ দেওয়া

```python
serializer = StudentSerializer(
    object,
    data=request.data
)
```

এখানে:

```text
object
↓
কোন Student-কে update করবো
```

আর:

```text
request.data
↓
কী নতুন data দিয়ে update করবো
```

---

### Step 4 — Data Valid কিনা Check

```python
if serializer.is_valid():
```

নতুন data ঠিক আছে কিনা check করলাম।

---

### Step 5 — Database Update

```python
serializer.save()
```

Valid হলে Database-এর Student-কে update করলাম।

---

### Step 6 — Response

```python
return Response(
    serializer.data,
    status=200
)
```

Updated Student-এর data return করলাম।

`200` মানে:

> **Successfully completed**

---

# 4. PATCH — Student-এর কিছু অংশ Update

```python
elif request.method == 'PATCH':

    student_id = request.data.get('id')

    object = Student.objects.get(
        id=student_id
    )

    serializer = StudentSerializer(
        object,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=200
        )

    return Response(
        serializer.errors,
        status=400
    )
```

### প্রথম অংশ PUT-এর মতোই

প্রথমে:

```python
student_id = request.data.get('id')
```

Request থেকে ID নিলাম।

তারপর:

```python
object = Student.objects.get(
    id=student_id
)
```

ওই ID দিয়ে Database থেকে Student object বের করলাম।

---

### মূল পার্থক্য এখানে

```python
partial=True
```

এর অর্থ:

> **Student-এর সব field দিতে হবে না। শুধু যে field পরিবর্তন করতে চাই সেটা দিলেই হবে।**

ধরো Student:

```json
{
    "id": 1,
    "name": "Rafi",
    "age": 25,
    "city": "Dhaka"
}
```

শুধু age পরিবর্তন করতে চাইলে PATCH:

```json
{
    "id": 1,
    "age": 26
}
```

এখানে `name` বা `city` আবার দিতে হবে না।

---

# PUT vs PATCH

## PUT

সাধারণভাবে **পুরো object update** করার জন্য ব্যবহার করা হয়।

```json
{
    "id": 1,
    "name": "Rafiul",
    "age": 26,
    "city": "Dhaka"
}
```

## PATCH

**Object-এর কিছু অংশ update** করার জন্য ব্যবহার করা হয়।

```json
{
    "id": 1,
    "age": 26
}
```

### মনে রাখার সহজ নিয়ম

```text
PUT   → পুরোটা Update
PATCH → কিছুটা Update
```

---

# 5. DELETE — Student Delete

```python
elif request.method == 'DELETE':

    student_id = request.data.get('id')

    object = Student.objects.get(
        id=student_id
    )

    object.delete()

    return Response(status=204)
```

### সহজভাবে

প্রথমে:

```python
student_id = request.data.get('id')
```

Request থেকে **ID নিলাম**।

তারপর:

```python
object = Student.objects.get(
    id=student_id
)
```

Student object থেকে ওই ID দিয়ে যে Student-এর ID মিলে, **সেই object-টা `object`-এর মধ্যে রাখলাম**।

তারপর:

```python
object.delete()
```

ওই Student-কে **Database থেকে delete করলাম**।

শেষে:

```python
return Response(status=204)
```

Response দিলাম।

`204` মানে:

> **Successfully completed, কিন্তু return করার মতো কোনো data নেই।**

---

# CRUD এক নজরে

| Method | কাজ            | সহজ ভাষা                   |
| ------ | -------------- | -------------------------- |
| GET    | Read           | Student নেওয়া              |
| POST   | Create         | Student তৈরি করা           |
| PUT    | Update         | পুরো Student update        |
| PATCH  | Partial Update | Student-এর কিছু অংশ update |
| DELETE | Delete         | Student delete করা         |

---

# সবচেয়ে গুরুত্বপূর্ণ Pattern

`PUT`, `PATCH`, `DELETE`-এর মধ্যে এই অংশটা খুব গুরুত্বপূর্ণ:

```python
student_id = request.data.get('id')

object = Student.objects.get(
    id=student_id
)
```

সহজ ভাষায়:

```text
Request থেকে ID নিলাম
        ↓
ID দিয়ে Database-এ Student খুঁজলাম
        ↓
Student object পেলাম
        ↓
এখন ওই object নিয়ে
Update / Delete করতে পারবো
```

### এরপর কাজ আলাদা

```text
PUT
→ Object + নতুন Data
→ পুরো Update
→ save()

PATCH
→ Object + নতুন Data
→ আংশিক Update
→ save()

DELETE
→ Object
→ delete()
```

---

# Status Code মনে রাখার Shortcut

```text
200 → Successfully completed

201 → Successfully Created

204 → Successfully completed
      কিন্তু Response-এর ভিতরে data নেই

400 → Bad Request
      অর্থাৎ Request-এর data-তে সমস্যা
```

---

# পুরো CRUD মনে রাখার Shortcut

```text
GET
→ Data নেওয়া

POST
→ Data তৈরি করা

PUT
→ পুরো Data Update

PATCH
→ কিছু Data Update

DELETE
→ Data Delete
```

## One Line Memory Trick

> **GET = নাও, POST = বানাও, PUT = পুরো বদলাও, PATCH = কিছু বদলাও, DELETE = মুছে ফেলো।**
