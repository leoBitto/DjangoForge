from django.db import models

class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    request_path = models.CharField(max_length=255)
    request_method = models.CharField(max_length=10)
    response_code = models.PositiveIntegerField()

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['request_path']),
            models.Index(fields=['response_code']),
        ]


class AccessRequestLog(RequestLog):
    def __str__(self):
        return f"Access at {self.timestamp}: {self.request_method} {self.response_code} {self.request_path}"


class ErrorRequestLog(RequestLog):
    error_message = models.TextField()
    stack_trace = models.TextField()

    def __str__(self):
        return f"Error at {self.timestamp}: {self.error_message}"
    



