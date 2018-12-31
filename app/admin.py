from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(City)
admin.site.register(Subject)
admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Category)
admin.site.register(Exam)
admin.site.register(Post)
admin.site.register(Comment)

