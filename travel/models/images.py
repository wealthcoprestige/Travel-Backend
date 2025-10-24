from setup.basemodel import BaseModel
from django.db import models
from travel.models.campaigns import Campaign

class CampaignImages(BaseModel):
    canpaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField()