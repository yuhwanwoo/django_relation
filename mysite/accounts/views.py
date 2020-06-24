from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm

# Create your views here.
def signup(request):    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    else: 
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            # AuthenticationForm은 ModelForm이 아닌 Form을 상속하기 때문에 생긴게 달라진다.
            # 별도로 정의된 Model이 없다는 뜻 => 고로 넘겨주는 인자가 달라진다.
            if form.is_valid():
                # 로그인은 DB에 뭔가 작성하는 것은 동일하지만 연결된 모듈이 있는 것은 아니다.
                # 그럼 확인해야 하는것은?
                #   => 세션과 유저정보를 확인해야 하기때문에
                #   => 세션(request)와 유저정보(form.get_user())를 확인해야 한다.
                auth_login(request, form.get_user())
                return redirect(request.GET.get('next') or 'articles:index')
        else:
            form = AuthenticationForm
        context = {
            'form' : form
        }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')

@require_POST
def delete(request):
    request.user.delete()
    return redirect('articles:index')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance = request.user)
    context={
        'form' : form
    }
    return render(request, 'accounts/update.html', context)
