from django.contrib import admin
from account.models import UserInfo, Token, PhoneFriend
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# Register your models here.

# Define an inline admin descriptor for UserInfo , Token model
# which acts a bit like a singleton
class UserInfoInline(admin.StackedInline):
    model = UserInfo
    can_delete = False
    verbose_name_plural = 'user_info'

class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')

class TokenInline(admin.StackedInline):
    model = Token
    can_delete = False
    verbose_name_plural = 'token'

class UserAdmin(UserAdmin):
    inlines = (UserInfoInline, TokenInline )

class PhoneFriendAdmin(admin.ModelAdmin):
	list_display = ('user', 'friend')

admin.site.register(UserInfo)
admin.site.register(Token, TokenAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(PhoneFriend, PhoneFriendAdmin)
