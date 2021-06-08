from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from rest_framework.authtoken.models import Token

from app.user.models import User



class UserAdmin(BaseUserAdmin):
    # inlines = (ProfileInline,TokenInline,ReglementInline )
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

    ordering = ['id']
    list_display = ["id","email", "username"]
    fieldsets = (
        (None, {'fields': 
            (   
                'email', 
                'password',
                'followings'
                )
            }
         ),
        
        (_('Personal Info'), 
         {'fields': (
             'username',
             'last_name',
             'first_name',
             )
          }
         ),
        
        (_('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        
        (_('Important dates'), 
         {'fields': (
             'last_login',
             )
          }
         ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

admin.site.register(User, UserAdmin)


