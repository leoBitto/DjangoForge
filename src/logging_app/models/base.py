from django.db import models

class Log(models.Model):
    timestamp = models.DateTimeField()
    request_path = models.CharField(max_length=255)
    request_method = models.CharField(max_length=10)
    response_code = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return f"Log at {self.timestamp}: {self.request_method} {self.request_path}"

class AccessLog(Log):
    pass

class ErrorLog(Log):
    error_message = models.TextField()
    stack_trace = models.TextField()

    def __str__(self):
        return f"Error at {self.timestamp}: {self.error_message}"
