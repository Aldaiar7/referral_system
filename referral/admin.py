from django.contrib import admin
from user.models import User
from .models import ReferralCode, ReferralRelationship

# Register your models here.
admin.site.register(User)
admin.site.register(ReferralRelationship)
admin.site.register(ReferralCode)
