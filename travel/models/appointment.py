from django.db import models, transaction, IntegrityError
from django.core.exceptions import ValidationError
from setup.basemodel import BaseModel
from travel.models.applicants import Applicant


class AvailableSlot(BaseModel):
    """Represents an interview time slot that can be booked."""
    date = models.DateField()
    time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=30)

    INTERVIEW_TYPES = [
        ("video", "Video Interview"),
        ("phone", "Phone Interview"),
        ("in_person", "In-Person Interview"),
    ]
    interview_type = models.CharField(
        max_length=20, choices=INTERVIEW_TYPES, default="video"
    )

    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} at {self.time} ({self.get_interview_type_display()})"


class BookedInterview(BaseModel):
    """Represents a booked interview with an applicant for a specific slot."""
    applicant = models.ForeignKey(
        Applicant,
        on_delete=models.CASCADE,
        related_name="booked_interviews",
        null=True,
        blank=True
    )
    customer_email = models.EmailField(null=True, blank=True)

    slot = models.OneToOneField(
        AvailableSlot,
        on_delete=models.CASCADE,
        related_name="booking",
    )

    description = models.TextField(null=True, blank=True)
    meeting_link = models.URLField(blank=True, null=True)

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )

    class Meta:
        # Safety net — ensures a slot can never have multiple bookings at the DB level
        constraints = [
            models.UniqueConstraint(fields=["slot"], name="unique_booking_per_slot"),
        ]

    def clean(self):
        """Validate slot availability before saving."""
        if self.slot.is_booked:
            raise ValidationError("This slot has already been booked.")

    def save(self, *args, **kwargs):
        self.slot.is_booked=True
        self.slot.save()
        return super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        """
        When a booking is deleted (cancelled or removed),
        mark the slot as available again.
        """
        with transaction.atomic():
            self.slot.is_booked = False
            self.slot.save()
            super().delete(*args, **kwargs)

    def __str__(self):
        return f"Interview on {self.slot.date} at {self.slot.time}"
