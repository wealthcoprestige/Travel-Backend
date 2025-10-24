from setup.basemodel import BaseModel
from django.contrib.auth import get_user_model
from travel.models.applicants import Applicant
from travel.models.campaigns import Campaign
from django.db import models
import uuid

User = get_user_model()


class Application(BaseModel):
    STATUS_CHOICES = [
        ("SUBMITTED", "Submitted"),
        ("UNDER_REVIEW", "Under Review"),
        ("INTERVIEW", "Interview Stage"),
        ("OFFERED", "Offered"),
        ("REJECTED", "Rejected"),
        ("WITHDRAWN", "Withdrawn"),
    ]
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    application_id= models.CharField(max_length=100, null=True, blank=True)
    campaign=models.ForeignKey(Campaign, on_delete=models.CASCADE)
    resume = models.FileField(null=True, blank=True)
    certification = models.FileField(null=True, blank=True)
    cover_letter = models.FileField(
        blank=True,
        null=True,
        help_text="Optional cover letter explaining motivation or suitability."
    )
    available_start_date = models.DateField(
        blank=True,
        null=True,
        help_text="When the applicant is available to start."
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SUBMITTED",
        help_text="Current status of the application process."
    )
    qualification = models.TextField(null=True, blank=True, help_text='enter any skill you have ')

    def save(self, *args, **kwargs):
        if not self.application_id:
            self.application_id = f"APP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


