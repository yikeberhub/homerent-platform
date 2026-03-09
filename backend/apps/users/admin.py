from django.contrib import admin

from apps.users.models import User,Credit

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'email',
        'name',
        'role',
        'is_verified',
        'created_at'
    )
    

# @admin.register(Credit)
# class CreditAdmin(admin.ModelAdmin):
    
#     list_display = (
#         'user',
#         'total_credits',
#         'used_credits'
#     )