from django.core.paginator import Paginator
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout, login
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Avg
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.db import models

import json

from .forms import UkrainianLoginForm, RegisterUserForm
from . import models
from .models import PopularTime, Post, Category, SubCategory, Hot, PopularDay, PopularSubCategory, Author, TableOrder, \
    PostMessage, Contact, Update, Rating


def nav_panel_sub():
    popular_sub_categorys = PopularSubCategory.objects.all()
    pop_sub_cats = []
    for pop_sub_cat in popular_sub_categorys:
        pop_sub_cats.append(pop_sub_cat)
    popular_sub_categorys = Paginator(pop_sub_cats, 6).page(1).object_list
    return popular_sub_categorys


def nav_panel_popular_time():
    popular = PopularTime.objects.all()
    populars = []
    for pop_time in popular:
        populars.append(pop_time)
    popular_time = Paginator(populars, 3).page(1).object_list  # пагінація бокової панелі Популярні
    return popular_time


def nav_panel_posts():
    posts = Post.objects.all()
    post_p = []
    for post_post in posts:
        post_p.append(post_post)
    posts = Paginator(post_p, 3).page(1).object_list  # пагінація бокової панелі Недавньо додані
    return posts


def pagin(request, post_dict):
    paginator = Paginator(post_dict, 12)  # пагінація бокової панелі Основних постів
    page_number = request.GET.get('page')
    posts_categ = paginator.get_page(page_number)
    return posts_categ


def home(request):
    popular = PopularTime.objects.all()
    hots = Hot.objects.all()
    populars_day = PopularDay.objects.all()

    hot = []
    popular_days = []
    populars = []

    for pop_time in popular:
        populars.append(pop_time)
    populars = Paginator(populars, 6).page(1).object_list

    for pop_day in populars_day:
        popular_days.append(pop_day)
    populars_day = Paginator(popular_days, 6).page(1).object_list

    for obj in hots:
        if obj.hot_name == 'True':
            for post in obj.post.all():
                hot.append(post)
    hot_post = Paginator(hot, 6).page(1).object_list

    context = {
        'populars': populars,
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'hot_post': hot_post,
        'populars_day': populars_day,
        'popular_sub_categorys': nav_panel_sub()
    }

    return render(request, 'home/home.html', context=context)


def new(request):
    posts = Post.objects.all()

    context = {
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'popular_sub_categorys': nav_panel_sub(),
        'title_header': 'Нещодавньо додані',
        'content_posts': pagin(request, posts),
        'number': len(pagin(request, posts)),
        'title': 'Нещодавньо додані книги',
    }

    return render(request, 'base_content_posts/base_content_posts.html', context=context)


def same_cat_posts(post):
    sub_cats = []
    for post_sub in post.sub_cat.all():
        sub_cats.append(post_sub)
    posts_sub_cat = []

    for sub_cat_p in sub_cats:
        for posts_same in Post.objects.filter(sub_cat=sub_cat_p):
            if posts_same not in posts_sub_cat:
                posts_sub_cat.append(posts_same)
    return posts_sub_cat


def popular_id(request, post_id):   # через селері дороб популярність на день
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        user = request.user
        message = request.POST.get('message')
        PostMessage.objects.create(message=message, user=user, post=post)

    posts_sub_cat = same_cat_posts(post)

    posts_sub_cat = Paginator(posts_sub_cat, 3).page(1).object_list
    author_posts = Paginator(post.author.post.all(), 3).page(1).object_list

    popular_time_update = post.popular_time
    popular_day_update = post.popular_day

    popular_time_update.popular_time = post.popular_time.popular_time + 1
    popular_day_update.popular_day = post.popular_day.popular_day + 1

    popular_time_update.save()
    popular_day_update.save()

    description_post = post.description
    paragraphs = description_post.split('\r\n\r\n')

    messages = PostMessage.objects.filter(post=post)

    context = {
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'popular_sub_categorys': nav_panel_sub(),

        'post': post,
        'posts_sub_cat': posts_sub_cat,
        'author_posts': author_posts,
        'paragraphs': paragraphs,
        'messages': messages
    }

    return render(request, 'popular_time/popular_time.html', context=context)


def selected(request):
    post_id = request.POST.get('post_id')
    post = Post.objects.get(id=post_id)

    if request.user in post.selected.all():
        post.selected.remove(request.user)
        result = False
    else:
        post.selected.add(request.user)
        result = True

    ctx = {'result': result}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def read(request):
    post_id = request.POST.get('post_id')
    post = Post.objects.get(id=post_id)

    if request.user in post.read.all():
        post.read.remove(request.user)
        result = False
    else:
        post.read.add(request.user)
        result = True

    ctx = {'result': result}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def popular(request):
    populars = PopularTime.objects.all()
    title_header = 'Популярні'
    content_posts = []

    for popular in populars:
            content_posts.append(popular.post)

    context = {
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'popular_sub_categorys': nav_panel_sub(),

        'title_header': title_header,
        'content_posts': pagin(request, content_posts),  # new
        'number': len(pagin(request, content_posts)),
        'title': 'Популярні книги',

    }
    return render(request, 'base_content_posts/base_content_posts.html', context=context)


def hot(request):
    hot = Hot.objects.filter(hot_name='True')
    title_header = 'Гарячі'
    content_posts = []

    for hot_cat in hot:
        for post in hot_cat.post.all():
            content_posts.append(post)

    context = {
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'popular_sub_categorys': nav_panel_sub(),
        'title_header': title_header,
        'content_posts': pagin(request, content_posts),  # new
        'number': len(pagin(request, content_posts)),
        'title': 'Гарячі книги',
    }

    return render(request, 'base_content_posts/base_content_posts.html', context=context)


def categories(request):
    categ = Category.objects.all()

    context = {
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'popular_sub_categorys': nav_panel_sub(),
        'categories': categ,
        'title': 'Категорії',
    }

    return render(request, 'categories/categories.html', context=context)


def update_news(request):
    updates = Update.objects.all()
    posts_ups = []
    posts_up = {}
    for update in updates:
        post = update.update_news

        posts_up[update] = post.split('\r\n')
    posts_ups.append(posts_up)

    context = {
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'popular_sub_categorys': nav_panel_sub(),
        'posts_ups': posts_ups,
    }

    return render(request, 'update/update.html', context=context)


def category_page(request, category):
    categ_posts = Category.objects.get(cat_url_name=category)
    posts_categ_set = categ_posts.cat.all()
    posts_categ = []

    for sub_cat in posts_categ_set: # перелічуєм підкатегорії
        for post in sub_cat.post.all():
            posts_categ.append(post)

    context = {
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'popular_sub_categorys': nav_panel_sub(),
        'title_header': f'{categ_posts.cat_name}',
        'content_posts': pagin(request, posts_categ),
        'number': len(pagin(request, posts_categ)),
        'title': f'{categ_posts.cat_name}',
    }

    return render(request, 'base_content_posts/base_content_posts.html', context=context)


def sub_category_page(request, category, sub_category):
    sub_category_object = SubCategory.objects.get(sub_cat_url_name=sub_category) # Популярне для підкатегорій
    sub_category_object.popular_sub_cat.popular_sub_category = sub_category_object.popular_sub_cat.popular_sub_category + 1
    sub_category_object.popular_sub_cat.save()

    categ_posts = SubCategory.objects.get(sub_cat_url_name=sub_category)
    posts_categ_set = categ_posts.post
    posts_categ = []

    for post in posts_categ_set.all():
        posts_categ.append(post)

    context = {
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'popular_sub_categorys': nav_panel_sub(),

        'title_header': f'{sub_category_object.sub_cat_name}',
        'content_posts': pagin(request, posts_categ),
        'number': len(pagin(request, posts_categ)),
        'title': f'{sub_category_object.sub_cat_name}',
    }

    return render(request, 'base_content_posts/base_content_posts.html', context=context)


def author(request, author_id):
    author = Author.objects.get(id=author_id)
    content_posts = author.post.all()

    context = {
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'popular_sub_categorys': nav_panel_sub(),

        'content_posts': content_posts,
        'title_header': author.author_name,
        'number': len(content_posts),
    }

    return render(request, 'base_content_posts/base_content_posts.html', context=context)


def search(request):
    if request.method == 'POST':
        search_obj = str(request.POST.get('search_obj'))
        content_posts = []
        author_list = []
        authors = Author.objects.all()

        for author in authors:
            if search_obj in author.author_name:
                author_list.append(author)
        for author in author_list:
            for post in author.post.all():
                content_posts.append(post)

        posts = Post.objects.all()
        for post in posts:
            if search_obj in post.post_name and post not in content_posts:
                content_posts.append(post)

        return HttpResponseRedirect(reverse('search_results') + f'?search_obj={search_obj}')

    return render(request, 'base_content_posts/base_content_posts.html')


def search_results(request):
    search_obj = request.GET.get('search_obj')

    content_posts = []
    author_list = []

    authors = Author.objects.all()

    for author in authors:
        if search_obj in author.author_name:
            author_list.append(author)
    for author in author_list:
        for post in author.post.all():
            content_posts.append(post)

    posts = Post.objects.all()
    for post in posts:
        if search_obj in post.post_name and post not in content_posts:
            content_posts.append(post)

    context = {
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'popular_sub_categorys': nav_panel_sub(),
        'title_header': f'Результат пошуку {search_obj}',
        'content_posts': content_posts,
        'number': len(content_posts),
        'title': f'Результат пошуку {search_obj}',
    }

    return render(request, 'base_content_posts/base_content_posts.html', context=context)


def support(request):
    return render(request, 'support/support.html')


def my_books(request):
    return render(request, 'my_books/my_books.html')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'login/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):  # для автоматичної авторизації після реєстрації
        user = form.save()
        login(self.request, user)
        return redirect('home')


class UkrainianLoginView(LoginView):
    form_class = UkrainianLoginForm
    template_name = 'login/login.html'

    def get_success_url(self):
        return reverse_lazy('my_books')


def logout_user(request):
    logout(request)
    return redirect('login')


def rate_post(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)  # Замініть 'YourApp' та 'Post' на свої значення
        stars = int(request.POST.get('stars', 0))

        # Перевірка, чи користувач вже голосував
        existing_rating = Rating.objects.filter(user=request.user, post=post)
        if existing_rating.exists():
            existing_rating.update(stars=stars)
        else:
            Rating.objects.create(user=request.user, post=post, stars=stars)

        # Розрахунок середнього рейтингу для відображення у шаблоні
        average_rating = Rating.objects.filter(post=post).aggregate(models.Avg('stars'))['stars__avg']

        return JsonResponse({'success': True, 'average_rating': average_rating})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request or user not authenticated'})


def get_rating(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    average_rating = Rating.objects.filter(post=post).aggregate(Avg('stars'))['stars__avg']

    return JsonResponse({'success': True, 'average_rating': average_rating})


def table_order(request):
    if request.method == 'POST':
        user = request.user
        message = request.POST.get('message')
        TableOrder.objects.create(message=message, user=user)

    messages = TableOrder.objects.all()

    context = {
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'popular_sub_categorys': nav_panel_sub(),

        'title_header': 'Стіл замовлень',
        'messages': messages,
        'title': 'Стіл замовлень',
    }

    return render(request, 'table_order/table_order.html', context=context)


def contact(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        title = request.POST.get('title')
        message = request.POST.get('message')
        Contact.objects.create(username=username, email=email, title=title, message=message)
        return JsonResponse({'result': True})

    return render(request, 'contact/contact.html')


def download_file_n(request):
    post_id = request.POST.get('post_id')
    post = Post.objects.get(id=post_id)
    post.number_of_downloads = post.number_of_downloads + 1
    post.save()
    return JsonResponse({'down_num': post.number_of_downloads})


def legal(request):
    return render(request, 'legal/legal.html')


def same_sub_cat(request, sub_cat):
    post = Post.objects.get(id=sub_cat)
    posts_sub_cat = same_cat_posts(post)

    context = {
        'popular_time': nav_panel_popular_time(),
        'posts': nav_panel_posts(),
        'popular_sub_categorys': nav_panel_sub(),

        'content_posts': posts_sub_cat,
        'title_header': 'Схожі книги',
        'number': len(posts_sub_cat),
    }

    return render(request, 'base_content_posts/base_content_posts.html', context=context)
