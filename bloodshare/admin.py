from django.contrib import admin
from .models import Profile, DonationRequest


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'city', 'is_available', 'last_donation_date', 'created_at')
    list_filter = ('blood_group', 'is_available', 'city', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'city', 'phone')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'requester', 'blood_group_needed', 'city', 'status', 'created_at')
    list_filter = ('status', 'blood_group_needed', 'city', 'created_at')
    search_fields = ('name', 'requester__username', 'requester__email', 'city', 'details')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
