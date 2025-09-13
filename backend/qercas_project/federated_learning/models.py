from django.db import models

class GlobalComplianceModel(models.Model):
    version = models.PositiveBigIntegerField(default=1)
    model_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Global Compliance Model v{self.version}"


