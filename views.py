from django.shortcuts import render, redirect, get_object_or_404
from triplog.models import Triplog
from django.contrib.auth.decorators import login_required 
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from triplog.create_map import create_map


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'triplog/signup.html'
    success_url = reverse_lazy('login')


@login_required
def index(request):
    all_data = Triplog.objects.all()
    context = {
        'title': '旅行の記録 - 一覧画面',
        'all_data': all_data,
    }
    return render(request, 'triplog/index.html', context)


def new(request):
    context = {
        'title' : '旅の記録 - 新規作成画面',
    }
    return render(request, 'triplog/new.html', context)


def create(request):
    if request.method == 'POST':
        triplog = Triplog(
            author = request.user, 
            title = request.POST['title'],
            content = request.POST['content'],
            latitude = request.POST['latitude'],
            longitude = request.POST['longitude'],        
        )
        triplog.save()
        messages.success(request, 'データを登録しました')
        return redirect('index')
    else:
        return redirect('index')


def detail(request, id):
    data = get_object_or_404(Triplog, pk=id)
    map = create_map(data.latitude, data.longitude)
    context = {
        'title': '旅の記録 - 詳細画面',
        'data': data,
        'map': map,
    }
    return render(request, 'triplog/detail.html', context)


def edit(request, id):
    data = get_object_or_404(Triplog, pk=id)
    context = {
        'title': '旅の記録 - 編集画面',
        'data': data,
    }
    return render(request, 'triplog/edit.html', context)


def update(request, id):
    if request.method == 'POST':
        edit_data = get_object_or_404(Triplog, pk=id)
        edit_data.title = request.POST['title']
        edit_data.content = request.POST['content']
        edit_data.latitude = request.POST['latitude']
        edit_data.longitude = request.POST['longitude']
        edit_data.save()    
        messages.success(request, 'データを更新しました')
        return redirect('index')
    else:
        return(redirect('index'))


def delete(request, id):
    delete_data = get_object_or_404(Triplog, pk=id)
    delete_data.delete()
    messages.success(request, 'データを削除しました')
    return redirect('index')
