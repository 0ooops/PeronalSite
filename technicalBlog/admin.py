from django.contrib import admin
from .models import PostCategory
from .models import Post

admin.site.register(PostCategory)
admin.site.register(Post)
