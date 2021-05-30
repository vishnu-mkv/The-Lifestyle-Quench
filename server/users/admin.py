from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserAdminCreateForm, UserAdminChangeForm, WriterApplicationForm, EmailActivationForm
from .models import User, WriterApplication, WriterProfile, UserProfile, EmailActivation
# Register your models here.
from .send_activation_email import send_activation_email


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreateForm
    readonly_fields = ['date_created']

    list_display = ('email', 'admin', 'active', 'staff', 'writer',)
    list_filter = ('admin', 'active', 'staff', 'writer',)
    fieldsets = (
        ('User', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active', 'writer',)}),
        ('Others', {'fields': ('date_created',)}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class WriterApplicationAdmin(admin.ModelAdmin):
    form = WriterApplicationForm

    readonly_fields = ['submitted_on', 'approved_by']

    fields = ('user', 'bio', 'writings', 'approved', 'submitted_on', 'approved_by',)

    def save_model(self, request, obj, form, change):
        if obj.approved:
            obj.approved_by = request.user
        obj.save()


class EmailActivationAdmin(admin.ModelAdmin):
    form = EmailActivationForm

    readonly_fields = ['key', 'email_sent', 'generated_on']

    fields = ('user', 'key', 'validity', 'email_sent', 'activated')

    def save_model(self, request, obj, form, change):
        print("user", obj.user, change)
        if not change:
            send_activation_email(obj.user)
            return
        obj.save()


# register here

admin.site.register(User, UserAdmin)
admin.site.register(WriterProfile)
admin.site.register(WriterApplication, WriterApplicationAdmin)
admin.site.register(UserProfile)
admin.site.register(EmailActivation, EmailActivationAdmin)

# Removing Group Model from admin. We're not using it.
admin.site.unregister(Group)
