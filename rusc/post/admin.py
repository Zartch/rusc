# -*- coding: utf-8 -*-
from django.contrib import admin
from rusc.post.models import Post,Vote

# Register your models here.

class postAdmin(admin.ModelAdmin):
    list_display = ('id','titol','autor','text')
    search_fields = ['titol','autor']
    list_filter = ['autor']
    filter_horizontal = ('etiquetes','recursos')


admin.site.register(Post, postAdmin)

class voteAdmin(admin.ModelAdmin):
    list_display = ('voter','post')
    search_fields = ['voter','post']
    list_filter = ['voter','post']

admin.site.register(Vote, voteAdmin)

# class PostRecursAdmin(admin.ModelAdmin):
#     list_display = ('post','recurs')
#     search_fields = ['post','recurs']
#     list_filter = ['post','recurs']
#
# admin.site.register(PostRecurs, PostRecursAdmin)
#
