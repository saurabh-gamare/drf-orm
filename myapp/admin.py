from django.contrib import admin
from .models import Teacher, Student, Blog, Author, Entry

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Entry)
