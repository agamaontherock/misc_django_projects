from django.contrib import admin
from chat_app.models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sent_on', 'user', 'room', 'content']
    list_filter = ['sent_on', 'room']
    search_fields = ['content']
    raw_id_fields = ['user']

# Register your models here.
