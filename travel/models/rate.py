from setup.basemodel import BaseModel
from django.db import models

class Rate(BaseModel):
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.amount)