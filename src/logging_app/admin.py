from django.contrib import admin
from .models import AccessLog, ErrorLog

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'request_path', 'request_method', 'response_code')
    search_fields = ('request_path',)
    list_filter = ('timestamp',)

@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'error_message', 'stack_trace')
    search_fields = ('error_message',)
    list_filter = ('timestamp',)
