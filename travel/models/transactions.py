from setup.basemodel import BaseModel
from travel.models.applicants import Applicant
from travel.models.billings import Billing
from travel.models.campaigns import Campaign
from django.db import models

class Transaction(BaseModel):
    STATUS = [
        ('pending', 'pending'),
        ('success', 'success'),
        ('failed', 'failed')
    ]
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    status = models.CharField(max_length=100, choices=STATUS)
    response = models.JSONField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Applicant: {self.applicant.full_name} Amount: {self.amount} Bill: {self.billing.name}"
