from django.contrib import admin
from .models import AccessRequestLog, ErrorRequestLog

@admin.register(AccessRequestLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'request_path', 'request_method', 'response_code')
    search_fields = ('request_path',)
    list_filter = ('timestamp',)

@admin.register(ErrorRequestLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'error_message', 'stack_trace')
    search_fields = ('error_message',)
    list_filter = ('timestamp',)
