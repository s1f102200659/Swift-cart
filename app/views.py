from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import Product
from app.models import Like
from app.models import Chat
from authtest.models import User
from .forms import UploadForm

# Create your views here.

def home(request, user_id):
    search = None
    results = None
    if request.method == 'POST':
        search = request.POST['search']
        results = Product.objects.filter(product_name__icontains=search, buyer_id=0)

    context = {
        "user": User.objects.get(id=user_id),
        "search": search,
        "results": results
    }
    categories = [1, 2, 3, 4, 5]
    for category in categories:
        key = f"products{category}"
        if ('sort' in request.GET):
            if request.GET['sort'] == 'posted_at':
                context[key] = Product.objects.filter(category=category, buyer_id=0).order_by('id')
            elif request.GET['sort'] == '-posted_at':
                context[key] = Product.objects.filter(category=category, buyer_id=0).order_by('-id')
            elif request.GET['sort'] == 'price':
                context[key] = Product.objects.filter(category=category, buyer_id=0).order_by('price')
            elif request.GET['sort'] == '-price':
                context[key] = Product.objects.filter(category=category, buyer_id=0).order_by('-price')
            elif request.GET['sort'] == 'like':
                context[key] = Product.objects.filter(category=category, buyer_id=0).order_by('like')
            elif request.GET['sort'] == '-like':
                context[key] = Product.objects.filter(category=category, buyer_id=0).order_by('-like')
        else:
            context[key] = Product.objects.filter(category=category, buyer_id=0).order_by('-id')

    return render(request, 'app/home.html', context)

def detail(request, user_id, prod_id):
    prod = Product.objects.get(id=prod_id)
    chat = Chat.objects.filter(product_id=prod_id)
    user = User.objects.get(id=user_id)
    try:
        buyer = User.objects.get(id=prod.buyer_id)
    except:
        buyer = None

    if request.method == 'POST':
        if 'review' in request.POST:
            review = request.POST['review']
            prod.review = review
            prod.save()
            user.points += 5
            user.save()
        elif 'comment' in request.POST:
            comment = request.POST['comment']
            new_chat = Chat(product_id=prod_id, writter_id=user_id, writter_name=user.user_name, comment=comment)
            new_chat.save()

    context = {
        "prod": prod,
        "seller": User.objects.get(id=prod.seller_id),
        "buyer": buyer,
        "user": user,
        "chat": chat,
        "chat_count": chat.count()
    }

    return render(request, 'app/detail.html', context)

def like(request, user_id, prod_id):
    prod = Product.objects.get(id=prod_id)
    try:
        like_objects = Like.objects.get(product_id=prod_id, user_id=user_id)
        if like_objects.is_liked == 0:
            prod.like += 1
            like_objects.is_liked = 1
        else:
            prod.like -= 1
            like_objects.is_liked = 0
        prod.save()
        like_objects.save()
    except:
        like_data = Like(product_id=prod_id, user_id=user_id, is_liked=1)
        prod.like += 1
        prod.save()
        like_data.save()

    return redirect(detail, user_id, prod_id)

def payment(request, user_id, prod_id):
    user = User.objects.get(id=user_id)
    prod = Product.objects.get(id=prod_id)
    error_message = None
    if request.method == 'POST':
        address = request.POST['address-pay']
        password = request.POST['password-pay']

        if user.address == address:
            if user.password == password:
                if user.points >= prod.price:
                    prod.buyer_id = user_id
                    prod.save()
                    user.points -= prod.price
                    user.save()
                else:
                    error_message = "ポイントが足りません"
            else:
                error_message = "パスワードが間違っています"
        else:
            error_message = "住所が間違っています"

    context = {
        "prod": prod,
        "user": user,
        "seller": User.objects.get(id=prod.seller_id),
        "error_message": error_message
    }

    return render(request, 'app/payment.html', context)

def sell(request, user_id):
    error_message = None
    if request.method == 'POST':
        try:
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                new_data = form.save(commit=False)
                new_data.id = Product.objects.all().count() + 1
                new_data.product_name = request.POST['product_name']
                new_data.category = request.POST['category']
                new_data.price = request.POST['price']
                new_data.seller_id = user_id
                new_data.comment = request.POST['comment']
                new_data.save()
                return redirect(home, user_id)
        except:
            error_message = "データの保存中にエラーが発生しました"

    context = {
        "upload_form": UploadForm(),
        "user": User.objects.get(id=user_id),
        "error_message": error_message
    }
    
    return render(request, 'app/sell.html', context)

def mypage(request, user_id):
    like_objects = Like.objects.filter(user_id=user_id)
    product_ids = []
    for object in like_objects:
        product_ids.append(object.product_id)

    context = {
        "like_prod": Product.objects.filter(id__in=product_ids),
        "bought_prod": Product.objects.filter(buyer_id=user_id),
        "sold_prod": Product.objects.filter(seller_id=user_id),
        "user": User.objects.get(id=user_id)
    }
    
    return render(request, 'app/mypage.html', context)

def charge(request, user_id):
    user = User.objects.get(id=user_id)
    error_message = None
    if request.method == 'POST':
        try:
            points = int(request.POST['points'])
            password = request.POST['password']
            if user.password == password:
                user.points += points
                user.save()
                return redirect('mypage', user_id)
            else:
                error_message = "パスワードが間違っています"
        except:
            error_message = "適切な金額を入力してください"

    context = {
        "user": user,
        "error_message": error_message
    }

    return render(request, 'app/charge.html', context)

def home_notlogin(request):
    search = None
    results = None
    products = None
    title = "新着商品"
    if request.method == 'POST':
        search = request.POST['search']
        results = Product.objects.filter(product_name__icontains=search, buyer_id=0)

    if ('sort' in request.GET):
        if request.GET['sort'] == 'posted_at':
            products = Product.objects.filter(buyer_id=0).order_by('id')
            title = "古い順"
        elif request.GET['sort'] == '-posted_at':
            products = Product.objects.filter(buyer_id=0).order_by('-id')
            title = "新しい順"
        elif request.GET['sort'] == 'price':
            products = Product.objects.filter(buyer_id=0).order_by('price')
            title = "値段（安い順）"
        elif request.GET['sort'] == '-price':
            products = Product.objects.filter(buyer_id=0).order_by('-price')
            title = "値段（高い順）"
        elif request.GET['sort'] == 'like':
            products = Product.objects.filter(buyer_id=0).order_by('like')
            title = "いいね（少ない順）"
        elif request.GET['sort'] == '-like':
            products = Product.objects.filter(buyer_id=0).order_by('-like')
            title = "いいね（多い順）"
    else:
        products = Product.objects.filter(buyer_id=0).order_by('-id')

    context = {
        "search": search,
        "results": results,
        "products": products,
        "title": title
    }

    return render(request, 'app/home_notlogin.html', context)

def home_Genre(request, user_id, productcategory):
    search = None
    results = None

    if request.method == 'POST':
        search = request.POST.get('search')
        results = Product.objects.filter(product_name__icontains=search, buyer_id=0 ,category = productcategory)

    context = {
        "user": User.objects.get(id=user_id),
        "search": search,
        "results": results
    }

    sort_key = f"products{productcategory}"
    categories_templates = {
        1: 'app/home_foods.html',
        2: 'app/home_clothes.html',
        3: 'app/home_acce.html',
        4: 'app/home_life.html',
        5: 'app/home_device.html',
    }

    category_filters = {
        'posted_at': 'id',
        '-posted_at': '-id',
        'price': 'price',
        '-price': '-price',
        'like': 'like',
        '-like': '-like'
    }

    category_id = int(productcategory)
    template = categories_templates.get(category_id)

    if template:
        product_filter = Product.objects.filter(category=category_id, buyer_id=0).order_by('-id')

        if 'sort' in request.GET:
            sort_option = request.GET['sort']
            sort_field = category_filters.get(sort_option)

            if sort_field:
                product_filter = product_filter.order_by(sort_field)

        context[sort_key] = product_filter

        return render(request, template, context)
    else:
        return HttpResponse("Invalid category")
