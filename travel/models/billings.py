from setup.basemodel import BaseModel
from travel.models.campaigns import Campaign
from travel.models.applicants import Applicant
from django.db import models

class Billing(BaseModel):
    CURRENCY = [
        ("$", "$"),
        ("£", "£"),
        ("₵", "₵"),
    ]
    STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
        ("cancelled", "Cancelled"),
    ]
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    currency = models.CharField(choices=CURRENCY, max_length=100)
    charged_currency = models.CharField(choices=CURRENCY, max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    charged_amount = models.DecimalField(decimal_places=2, max_digits=20)
    status = models.CharField(max_length=100, choices=STATUS)

    def __str__(self):
        return f"Applicant: {self.applicant.full_name} Campaign: {self.campaign.title}"