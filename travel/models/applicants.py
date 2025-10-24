from setup.basemodel import BaseModel
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Applicant(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email=models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=100)
    whats_app = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100)
    passport_number= models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    id_card = models.CharField(max_length=100)
    card_image_front = models.ImageField(default=list, help_text='upload front of the id card')
    card_image_back = models.ImageField(default=list, help_text='upload back of the id card')
    
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text="Applicant's date of birth."
    )
    profile_photo = models.ImageField(
        blank=True,
        null=True,
        help_text="Optional profile photo of the applicant."
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="Brief summary or professional bio."
    )
    linkedin_profile = models.URLField(
        blank=True,
        null=True,
        help_text="Link to applicant's LinkedIn profile."
    )
    website_or_portfolio = models.URLField(
        blank=True,
        null=True,
        help_text="Link to personal website or professional portfolio."
    )
    languages_spoken = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Languages spoken fluently (comma-separated)."
    )
    education = models.TextField(
        blank=True,
        null=True,
        help_text="Education background or degrees obtained."
    )
    def save(self, *args, **kwargs):
        if not self.user:
            user = User.objects.create(
                username=self.full_name,
                email=self.email
            )
            user.set_password(f'{self.full_name}12345')
            self.user=user
            user.save()
            

        return super().save(*args, **kwargs)


    def __str__(self):
        return self.full_name