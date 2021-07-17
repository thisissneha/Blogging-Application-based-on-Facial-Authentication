from django.contrib import admin
from home.models import Contact, Profile, Preference, VerifyEmail

# Register your models here.
admin.site.register(Contact)
admin.site.register(Profile)
admin.site.register(Preference)
admin.site.register(VerifyEmail)
