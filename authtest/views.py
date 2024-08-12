from django.shortcuts import render, redirect
from django.urls import reverse
from app.views import home
from authtest.models import User

# Create your views here.

def login(request):
    error_message = None
    if request.method == 'POST':
        user_name = request.POST['user_name']
        password = request.POST['password']

        try:
            user = User.objects.get(user_name=user_name)
            if user.password == password:
                return redirect(home, user.id)
            else:
                error_message = "パスワードが間違っています"
        except:
            error_message = "ユーザーが存在しません"

    context = {
        "error_message": error_message
    }

    return render(request, 'authtest/login.html', context)

def account(request):
    error_message = None
    if request.method == 'POST':
        id = User.objects.all().count() + 1
        user_name = request.POST['user_name']
        password = request.POST['password']
        full_name = request.POST['full_name']
        birth = request.POST['birth']
        address = request.POST['address']
        post = request.POST['post']
        tel = request.POST['tel']
        mail = request.POST['mail']

        if User.objects.filter(user_name=user_name).exists():
            error_message = "このユーザーネームは既に使用されています"
        elif User.objects.filter(password=password).exists():
            error_message = "このパスワードは既に使用されています"
        else:
            try:
                new_data = User(id=id, user_name=user_name, password=password, full_name=full_name, birth=birth,
                            address=address, post=post, tel=tel, mail=mail, points=0)
                new_data.save()
                return redirect(login)
            except:
                error_message = "データの保存中にエラーが発生しました"

    context = {
        "error_message": error_message
    }

    return render(request, 'authtest/account.html', context)
