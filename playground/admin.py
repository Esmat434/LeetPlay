from django.contrib import admin
from .models import Question,Solved
# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title','category','tag','slug','is_enable','created_time')
    list_filter = ('category','tag','is_enable')
    search_fields = ('title','category','tag')
    ordering = ('category','tag','is_enable')

    # def has_add_permission(self, request):
    #     return True

    # def has_change_permission(self, request, obj = ...):
    #     return True
    
    # def has_delete_permission(self, request, obj = ...):
    #     return True

@admin.register(Solved)
class SolvedAdmin(admin.ModelAdmin):
    list_display = ['user','question']

    # def has_add_permission(self, request):
    #     return False

    # def has_change_permission(self, request, obj = ...):
    #     return False

    # def has_delete_permission(self, request, obj = ...):
    #     return False