from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(PostComment)
admin.site.register(Skills)
admin.site.register(OtherSkill)