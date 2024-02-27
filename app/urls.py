from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('new', new, name='new'),

    path('popular', popular, name='popular'),

    path('book/<int:post_id>', popular_id, name='popular_id'),
    path('same_sub_cat/<int:sub_cat>', same_sub_cat, name='same_sub_cat'),

    path('hot', hot, name='hot'),
    path('categories', categories, name='categories'),
    path('update_news', update_news, name='update_news'),

    path('categories/<str:category>', category_page, name='category-page'),
    path('categories/<str:category>/<str:sub_category>', sub_category_page, name='sub_category-page'),

    path('author/<str:author_id>', author, name='author'),
    path('search', search, name='search'),
    path('search/results/', search_results, name='search_results'),
    path('support', support, name='support'),
    path('my_books', my_books, name='my_books'),

    path('register', RegisterUser.as_view(), name='register'),
    path('login', UkrainianLoginView.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('selected', selected, name='selected'),
    path('read', read, name='read'),

    path('rate/<int:post_id>/', rate_post, name='rate_post'),
    path('get_rating/<int:post_id>/', get_rating, name='get_rating'),

    path('table_order', table_order, name='table_order'),
    path('contact', contact, name='contact'),

    path('download_file_n', download_file_n, name='download_file_n'),
    path('legal', legal, name='legal'),
]
