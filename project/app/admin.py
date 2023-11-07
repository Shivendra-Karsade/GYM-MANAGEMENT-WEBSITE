from django.contrib import admin
from .models import Registration,Query
# Register your models here.


class RegisterAdmin(admin.ModelAdmin):
    list_display=('name','email','age','phone','amount','order_id','paid')

admin.site.register(Registration,RegisterAdmin)

class QueryAdmin(admin.ModelAdmin):
    list_display=('name','email','message')

admin.site.register(Query,QueryAdmin)