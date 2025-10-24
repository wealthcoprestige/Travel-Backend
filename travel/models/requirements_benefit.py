from setup.basemodel import BaseModel
from travel.models.campaigns import Campaign
from django.db import models


class RequirementBenefit(BaseModel):
    compagin = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='campaign_benefits')
    short_description = models.TextField(max_length=500)
    full_description = models.TextField()
    requirements = models.JSONField(
        default=list, help_text="List of requirements as JSON"
    )
    responsibilities = models.JSONField(
        default=list, blank=True, help_text="List of responsibilities as JSON"
    )
    preferred_qualifications = models.JSONField(
        default=list, blank=True, help_text="Preferred qualifications as JSON"
    )
    benefit = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return self.short_description
