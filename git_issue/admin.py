from django.contrib import admin

from .models import Question,Issue,Customer,Solve
# Register your models here.
admin.site.register(Issue)
admin.site.register(Question)
admin.site.register(Customer)
admin.site.register(Solve)