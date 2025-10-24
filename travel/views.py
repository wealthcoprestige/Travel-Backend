from rest_framework import viewsets
from travel.models.applicants import Applicant
from travel.models.applications import Application
from travel.models.appointment import *
from travel.models.campaigns import Campaign
from travel.models.categories import Category
from travel.models.requirements_benefit import RequirementBenefit
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from travel.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from travel.models.billings import Billing
from travel.pay_config import *
from django.shortcuts import redirect
import random
import string


def generate_reference(length: int = 10) -> str:
    """Generate a random transaction reference string."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializers


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializers


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = AvailableSlot.objects.all()
    serializer_class = AppointmentSerializers


class BookedInterviewViewSet(viewsets.ModelViewSet):
    queryset = BookedInterview.objects.all()
    serializer_class = BookedInterviewSerializers
    permission_classes = [AllowAny]


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializers

    def create(self, request, *args, **kwargs):
        return Response(
            {"details": "create method is not allowed"},
            status=status.HTTP_403_FORBIDDEN,
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [AllowAny]


class RequirementBenefitViewSet(viewsets.ModelViewSet):
    queryset = RequirementBenefit.objects.all()
    serializer_class = RequirementBenefitSerializers


class CampaignDetailsAPIView(GenericAPIView):
    serializer_class = CampaignSerializers
    permission_class = [AllowAny]

    def get_campaign_benefits(self, campaign):
        benefits_and_requirements = campaign.campaign_benefits.all()
        return RequirementBenefitSerializers(benefits_and_requirements, many=True).data

    def get_campaign_images(self, compaign, request):
        campaign_gallery = compaign.gallery.all()
        return CampaignImagesSerializer(
            campaign_gallery, many=True, context={"request": request}
        ).data

    def get(self, request, campaign_id):
        campaign = get_object_or_404(Campaign, id=campaign_id)

        return Response(
            {
                "campaign": CampaignSerializers(campaign).data,
                "gallery": self.get_campaign_images(campaign, request),
                "compaign_benefits": self.get_campaign_benefits(campaign),
            }
        )


class CreateApplicationAuthenticatedApplicant(GenericAPIView):
    serializer_class = ApplicationSerializers
    permission_classes = [AllowAny]

    def create_authenticated_user_application(self, applicant, campaign):
        application = Application.objects.create(applicant=applicant, campaign=campaign)
        return application

    def post(self, request, campaign_id):
        campaign = get_object_or_404(Campaign, id=campaign_id)

        if not request.user:
            return Response(
                {"message": "you dont have the permission to perform this action"}, 400
            )

        applicant = get_object_or_404(Applicant, user=request.user)
        if self.create_authenticated_user_application(applicant, campaign):
            return Response({"message": "Application submitted successfully"}, 200)
        return Response(
            {"message": "failed creating processing application, Try again later"}, 400
        )


class CreateApplicantApplicationAPIView(GenericAPIView):
    serializer_class = CreateCustomerApplicationSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(auto_schema=None)
    def post(self, request, campaign_id):
        campaign = get_object_or_404(Campaign, id=campaign_id)

        serializer = self.serializer_class(
            data=request.data, context={"campaign": campaign}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Application submitted here successfully"},
                status=200,
            )

        return Response(serializer.errors, status=400)


class ApplicantDashboardAPIView(GenericAPIView):
    serializer_class = ApplicantSerializers
    permission_calsses = [IsAuthenticated]

    def get_applicant_biling(self, applicant):
        billing = Billing.objects.filter(applicant=applicant)
        return BillingSerializers(billing, many=True).data

    def get_applicant_interview_appointment(self, applicant):
        interview_appointments = BookedInterview.objects.filter(applicant=applicant)
        return BookedInterviewSerializers(interview_appointments, many=True).data

    def get_applicant_applications(self, applicant, request):
        application = Application.objects.filter(applicant=applicant)
        return ApplicationSerializers(
            application, many=True, context={"request": request}
        ).data

    def get(self, request):
        applicant = get_object_or_404(Applicant, user=request.user)

        return Response(
            {
                "applicant": ApplicantSerializers(
                    applicant, context={"request": request}
                ).data,
                "applicant_applicantions": self.get_applicant_applications(
                    applicant, request
                ),
                "applicant_appointment": self.get_applicant_interview_appointment(
                    applicant
                ),
                "applicant_appointment": self.get_applicant_interview_appointment(
                    applicant
                ),
                "applicant_billings": self.get_applicant_biling(applicant),
            }
        )


class BillPaymentAPIView(GenericAPIView):
    serializer_class = ProcessPaymentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, bill_id):
        bill = get_object_or_404(Billing, id=bill_id, applicant__user=request.user)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data["amount"]

            transaction = Transaction.objects.create(
                applicant=bill.applicant,
                campaign=bill.campaign,
                billing=bill,
                amount=amount,
                status="pending",
                transaction_id=generate_reference(),
            )

            callback_url = request.build_absolute_uri("/verify/transaction/applicant")
            raw_response = process_payment(
                transaction, callback_url, float(transaction.amount)
            )
            print(raw_response.json())

            try:
                data = raw_response.json()
            except ValueError:
                return Response(
                    {"message": "Invalid response from payment processor."},
                    status=502,
                )

            if data.get("success"):
                return Response(
                    {"success": True, "redirect_url": data.get("redirect_url")}, 200
                )

            return Response(
                {"message": "Failed to process payment. Try again later."},
                status=400,
            )
        return Response(serializer.errors, status=400)


class VerifyTransactionAPIView(GenericAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        reference = request.GET.get("reference")
        if not reference:
            return Response(
                {"message": "Missing transaction reference."},
                status=400,
            )

        result = confirm_transaction(reference)

        if (
            result.get("success")
            and result.get("data", {}).get("status", "").lower() == "success"
        ):
            transaction = get_object_or_404(Transaction, transaction_id=reference)
            billing = transaction.billing

            billing.charged_amount -= transaction.amount
            if billing.amount <= 0:
                billing.status = "paid"

            billing.save()

            transaction.status = "success"
            transaction.save()

            return Response(
                {"message": "Payment completed successfully."},
                status=200,
            )

        return Response(
            {
                "message": "Failed verifying transaction.",
                "details": result,
            },
            status=400,
        )


class AvalableAppointmentSlotAPIView(GenericAPIView):
    serializer_class = AppointmentSerializers
    permission_classes = [AllowAny]

    def get(self, request):
        available_slot = AvailableSlot.objects.filter(is_booked=False)

        return Response(self.serializer_class(available_slot, many=True).data, 200)


class ApplicantInterViewAppointmentAPIView(GenericAPIView):
    serializer_class = AppointmentSerializers
    permaission_classes = [AllowAny]

    def get(self, user_email):
        appointment = AvailableSlot.objects.filter(customer_email=user_email)

        return Response(self.serializers_class(appointment, many=True).data)
