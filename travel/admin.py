from django.contrib import admin
from travel.models.campaigns import Campaign
from travel.models.applicants import Applicant
from travel.models.applications import Application
from travel.models.categories import Category
from travel.models.requirements_benefit import RequirementBenefit
from travel.models.appointment import AvailableSlot, BookedInterview
from travel.models.images import CampaignImages
from travel.models.billings import Billing
from travel.models.transactions import Transaction
from travel.models.rate import Rate

# Register your models here.


admin.site.register(Category)
admin.site.register(Campaign)
admin.site.register(RequirementBenefit)
admin.site.register(Applicant)
admin.site.register(Application)
admin.site.register(BookedInterview)
admin.site.register(AvailableSlot)
admin.site.register(CampaignImages)
admin.site.register(Billing)
admin.site.register(Transaction)
admin.site.register(Rate)
