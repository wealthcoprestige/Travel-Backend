from rest_framework import serializers
from travel.models.applicants import Applicant
from travel.models.applications import Application
from travel.models.campaigns import Campaign
from travel.models.categories import Category
from travel.models.requirements_benefit import RequirementBenefit
from travel.models.appointment import *
from travel.models.images import CampaignImages
from travel.utils import AbsoluteImageUrlMixin
from travel.models.billings import Billing
from django.contrib.auth import get_user_model
from travel.models.transactions import Transaction

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "is_admin",
            "is_staff",
            "is_superuser",
            "is_applicant",
            "last_login",
            "is_active",
            "password",
        ]


class BookedInterviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookedInterview
        fields = "__all__"





class CreateApplicationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Application
        exclude = [
            "applicant",
            "campaign",
            "application_id",
            "status",
            "created_at",
            "updated_at",
        ]


class BillingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = "__all__"


class ApplicantSerializers(AbsoluteImageUrlMixin, serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Applicant
        fields = "__all__"


class CreateApplicantSerializers(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        exclude = ["user", "created_at", "updated_at"]


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CampaignSerializers(serializers.ModelSerializer):
    category = CategorySerializers()

    class Meta:
        model = Campaign
        fields = "__all__"


class ApplicationSerializers(AbsoluteImageUrlMixin, serializers.ModelSerializer):
    campaign = CampaignSerializers()
    class Meta:
        model = Application
        fields = "__all__"

class RequirementBenefitSerializers(serializers.ModelSerializer):
    class Meta:
        model = RequirementBenefit
        fields = "__all__"


class AppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlot
        fields = "__all__"


class BookedInterviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookedInterview
        exclude = ["status"]


class CampaignImagesSerializer(AbsoluteImageUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = CampaignImages
        fields = "__all__"


class CreateCustomerApplicationSerializer(serializers.Serializer):

    full_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=100)
    passport_number = serializers.CharField(max_length=100)
    nationality = serializers.CharField(max_length=100)
    id_card = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=False, allow_null=True)
    whats_app = serializers.CharField(required=False, allow_null=True, max_length=100)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    profile_photo = serializers.ImageField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_null=True)
    linkedin_profile = serializers.URLField(required=False, allow_null=True)
    website_or_portfolio = serializers.URLField(required=False, allow_null=True)
    languages_spoken = serializers.CharField(
        required=False, allow_null=True, max_length=255
    )
    education = serializers.CharField(required=False, allow_null=True)
    card_image_front = serializers.ImageField(required=False)
    card_image_back = serializers.ImageField(required=False)

    resume = serializers.FileField(required=False, allow_null=True)
    certification = serializers.FileField(required=False, allow_null=True)
    cover_letter = serializers.FileField(required=False, allow_null=True)
    available_start_date = serializers.DateField(required=False, allow_null=True)
    qualification = serializers.CharField(required=False, allow_null=True)

    def validate(self, data):
        email = data.get("email")
        campaign = self.context.get("campaign")

        if email and campaign:
            if Application.objects.filter(
                applicant__email=email, campaign=campaign
            ).exists():
                raise serializers.ValidationError(
                    {"applicant": "You have already applied to this job."}
                )
        return data

    def create(self, validated_data):

        applicant_fields = [
            "full_name",
            "phone_number",
            "location",
            "passport_number",
            "nationality",
            "id_card",
            "email",
            "whats_app",
            "date_of_birth",
            "profile_photo",
            "bio",
            "linkedin_profile",
            "website_or_portfolio",
            "languages_spoken",
            "education",
            "card_image_front",
            "card_image_back",
        ]

        application_fields = [
            "resume",
            "certification",
            "cover_letter",
            "available_start_date",
            "qualification",
        ]

        applicant_data = {
            field: validated_data.get(field) for field in applicant_fields
        }
        application_data = {
            field: validated_data.get(field) for field in application_fields
        }

        campaign = self.context.get("campaign")

        applicant_serializer = CreateApplicantSerializers(data=applicant_data)
        applicant_serializer.is_valid(raise_exception=True)
        applicant = applicant_serializer.save()

        application_serializer = CreateApplicationSerializers(data=application_data)
        application_serializer.is_valid(raise_exception=True)
        application = application_serializer.save(
            applicant=applicant, campaign=campaign
        )

        return {"applicant": applicant, "application": application}


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ["transaction_id", "status", "applicant", "campaign"]


class ProcessPaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(decimal_places=2, max_digits=20)

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("entr a valid amount")
        return amount
