from django.contrib import admin
from .models import Post, PopularDay, PopularTime, SubCategory, Category, Hot, PopularSubCategory, \
    Language, TypeFile, Author, Rating, TableOrder, PostMessage, Contact, Update

admin.site.register(Post)
admin.site.register(PopularDay)
admin.site.register(PopularTime)
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(Hot)
admin.site.register(PopularSubCategory)
admin.site.register(Language)
admin.site.register(TypeFile)
admin.site.register(Author)
admin.site.register(Rating)
admin.site.register(TableOrder)
admin.site.register(PostMessage)
admin.site.register(Contact)
admin.site.register(Update)
