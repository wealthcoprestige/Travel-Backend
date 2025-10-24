from django.db import models
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract =True
        ordering = ['-created_at']