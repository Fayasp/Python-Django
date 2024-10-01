from django.contrib import admin

from .models import Address, Members, Post

# Register your models here.

admin.site.register(Post)
admin.site.register(Members)
admin.site.register(Address)
