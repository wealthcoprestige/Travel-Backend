from setup.basemodel import BaseModel
from django.db import models

class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name