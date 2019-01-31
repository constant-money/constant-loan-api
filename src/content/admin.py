from django.contrib import admin

from content.models import EmailContent, SMSContent


@admin.register(EmailContent)
class EmailContentAdmin(admin.ModelAdmin):
    list_display = ['purpose', 'language', 'subject', 'updated_at']
    list_filter = ('language', 'purpose', )


@admin.register(SMSContent)
class SMSContentAdmin(admin.ModelAdmin):
    list_display = ['purpose', 'language', 'content', 'updated_at']
    list_filter = ('purpose',)
