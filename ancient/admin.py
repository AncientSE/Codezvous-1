
from django.contrib import admin
from .models import Submit, Identity, ClassTable, ClassChoose, Homework,newuser
@admin.register(newuser)
class newuserAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','password')
    ordering = ('id',)

admin.site.register(Submit)
admin.site.register(Identity)
admin.site.register(ClassTable)
admin.site.register(ClassChoose)
admin.site.register(Homework)