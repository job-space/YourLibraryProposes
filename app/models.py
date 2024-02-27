from django.db import models
from django.contrib.auth.models import User


class PopularSubCategory(models.Model):
    popular_sub_category = models.IntegerField(default=0)
    sub_cat_name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.sub_cat_name

    class Meta:
        ordering = ['-popular_sub_category']


class Category(models.Model):
    cat_name = models.CharField(max_length=100, null=False, blank=False)
    cat_url_name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.cat_name


class SubCategory(models.Model):
    sub_cat_name = models.CharField(max_length=100, null=False, blank=False)
    sub_cat_url_name = models.CharField(max_length=100, null=False, blank=False)

    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat')
    popular_sub_cat = models.OneToOneField(PopularSubCategory, on_delete=models.CASCADE, related_name='sub_category')

    def __str__(self):
        return self.sub_cat_name


class Hot(models.Model):
    hot_name = models.CharField(max_length=100, null=False, blank=False)
    data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hot_name

    class Meta:
        ordering = ['-data']


class PopularDay(models.Model):
    popular_day_post_name = models.CharField(max_length=100, null=True)
    popular_day = models.IntegerField(default=0)

    def __str__(self):
        return self.popular_day_post_name

    class Meta:
        ordering = ['-popular_day']


class PopularTime(models.Model):
    popular_time_post_name = models.CharField(max_length=100, null=True)
    popular_time = models.IntegerField(default=0)

    def __str__(self):
        return self.popular_time_post_name

    class Meta:
        ordering = ['-popular_time']


class Language(models.Model):
    language_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.language_name

    class Meta:
        ordering = ['-language_name']


class TypeFile(models.Model):
    file_for_post = models.CharField(max_length=100, null=True)
    type_file_name = models.CharField(max_length=100, null=True)
    file_object = models.FileField(upload_to=f"file_book_d/%Y/%m/%d/", null=True)

    def __str__(self):
        return self.file_for_post

    class Meta:
        ordering = ['-file_for_post']


class Author(models.Model):
    author_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.author_name

    class Meta:
        ordering = ['-author_name']


class Post(models.Model):
    post_image = models.ImageField(upload_to=f"menu_image/%Y/%m/%d/")
    post_name = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now=True)

    description = models.TextField()
    graduation_year = models.DateTimeField()
    number_of_downloads = models.IntegerField(default=0)
    number_of_pages = models.IntegerField(default=0)

    popular_day = models.OneToOneField(PopularDay, on_delete=models.CASCADE, related_name='post')
    popular_time = models.OneToOneField(PopularTime, on_delete=models.CASCADE,  related_name='post')

    sub_cat = models.ManyToManyField(SubCategory, related_name='post')

    hot = models.ManyToManyField(Hot, blank=True, related_name='post')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='post', null=True)
    type_file = models.ManyToManyField(TypeFile, related_name='post', null=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='post', blank=True, null=True)

    read = models.ManyToManyField(User, related_name='read', blank=True)
    selected = models.ManyToManyField(User, related_name='selected', blank=True)

    def __str__(self):
        return self.post_name

    class Meta:
        ordering = ['-data']


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)

    def __str__(self):
        return self.post.post_name


class TableOrder(models.Model):
    message = models.TextField(blank=True)
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table_order')

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-data']


class PostMessage(models.Model):
    message = models.TextField(blank=True)
    data = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_message')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_message')

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-data']


class Contact(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    title = models.CharField(max_length=100)
    message = models.TextField(blank=False)

    def __str__(self):
        return self.title


class Update(models.Model):
    update_news = models.TextField()
    image_news = models.ImageField(upload_to=f"image_news/%Y/%m/%d/")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.update_news

    class Meta:
        ordering = ['-date']
