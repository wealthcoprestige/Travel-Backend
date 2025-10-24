from rest_framework.routers import DefaultRouter
from django.urls import path, include
from travel.views import *

router = DefaultRouter()
router.register(r"applicants", ApplicantViewSet)
router.register(r"applications", ApplicationViewSet)
router.register(r"appointments", AppointmentViewSet)
router.register(r"campaigns", CampaignViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"requirement-benefits", RequirementBenefitViewSet)
router.register(r"book-applicant-appointment", BookedInterviewViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "compaign/details/<uuid:campaign_id>",
        CampaignDetailsAPIView.as_view(),
        name="campaign",
    ),
    path(
        "create/applicant/application/unauthenticated/<uuid:campaign_id>",
        CreateApplicantApplicationAPIView.as_view(),
        name="create_applicant_application",
    ),
    path(
        "dashboard/applicant/",
        ApplicantDashboardAPIView.as_view(),
        name="dashboard_applicant",
    ),
    path(
        "processes/applicant/payment/<uuid:bill_id>",
        BillPaymentAPIView.as_view(),
        name="process_applicant_payment",
    ),
    path(
        "verify/transaction/applicant",
        VerifyTransactionAPIView.as_view(),
        name="verify_transaction",
    ),
    path(
        "available/appointment/slot/",
        AvalableAppointmentSlotAPIView.as_view(),
        name="available_slot",
    ),
    path(
        "applicant/appointments/<str:user_email>",
        ApplicantInterViewAppointmentAPIView.as_view(),
        name="applicant_appointments",
    ),
    path(
        "applicant/application/auth/<uuid:campaign_id>",
        CreateApplicationAuthenticatedApplicant.as_view(),
        name="applicant_appointments",
    ),
]
