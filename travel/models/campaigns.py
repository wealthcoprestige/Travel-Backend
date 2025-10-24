from setup.basemodel import BaseModel
from travel.models.categories import Category
from django.db import models


class Campaign(BaseModel):
    EMPLOYMENT_TYPE_CHOICES = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("contract", "Contract"),
        ("temporary", "Temporary"),
        ("internship", "Internship"),
        ("remote", "Remote"),
    ]
    EXPERIENCE_LEVEL_CHOICES = [
        ("entry", "Entry Level"),
        ("mid", "Mid Level"),
        ("senior", "Senior Level"),
        ("executive", "Executive"),
        ("student", "Student"),
    ]
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("closed", "Closed"),
        ("expired", "Expired"),
    ]
    REMOTE = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("closed", "Closed"),
        ("expired", "Expired"),
    ]
    image = models.ImageField()
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    remote = models.CharField(default="on site", choices=REMOTE, max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    employment_type = models.CharField(
        max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, blank=True
    )
    experience_level = models.CharField(
        max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, blank=True
    )
    duration = models.CharField(
        max_length=100, blank=True, help_text="e.g., Full-time, 12 months, etc."
    )

    def __str__(self):
        return self.title
