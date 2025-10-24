import os
import tempfile
import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from travel.models.campaigns import Campaign
from travel.models.categories import Category
from travel.models.images import CampaignImages


class Command(BaseCommand):
    help = "Seeds the database with international job and relocation campaigns (UUID safe)"

    def handle(self, *args, **options):
        categories_to_create = ["Healthcare", "Education", "Public Health", "Scholarships", "NGO Programs"]
        category_map = {}
        for name in categories_to_create:
            category, _ = Category.objects.get_or_create(name=name)
            category_map[name] = category

        campaigns = [
  {
    "title": "Certified Nursing Assistant (CNA) – Canada Relocation Program",
    "location": "Toronto General Hospital",
    "remote": "on site",
    "country": "Canada",
    "city": "Toronto",
    "state": "Ontario",
    "description": "Join one of Canada’s leading healthcare institutions as a Certified Nursing Assistant. This position is part of our international relocation program for qualified healthcare professionals.",
    "status": "published",
    "employment_type": "full_time",
    "experience_level": "entry",
    "duration": "Permanent",
    "category": "UUID_HERE",
    "image_gallery": [
      "https://images.unsplash.com/photo-1580281657527-47d7c0a5f2f0",
      "https://images.unsplash.com/photo-1597764699515-0b1d48a5a8a1"
    ]
  },
  {
    "title": "Physician Assistant – UK NHS Visa Sponsorship",
    "location": "King’s College Hospital",
    "remote": "on site",
    "country": "United Kingdom",
    "city": "London",
    "state": "",
    "description": "The NHS is recruiting Physician Assistants for its international talent program. This role includes full visa sponsorship and relocation support.",
    "status": "published",
    "employment_type": "full_time",
    "experience_level": "mid",
    "duration": "3-year contract",
    "category": "UUID_HERE",
    "image_gallery": [
      "https://images.unsplash.com/photo-1607746882042-944635dfe10e",
      "https://images.unsplash.com/photo-1576765607924-bd7ca748754d"
    ]
  },
  {
    "title": "Healthcare Assistant (HCA) – Germany Integration Program",
    "location": "Charité – Universitätsmedizin Berlin",
    "remote": "on site",
    "country": "Germany",
    "city": "Berlin",
    "state": "",
    "description": "Work as a Healthcare Assistant in Berlin with training, German language support, and relocation assistance provided for foreign applicants.",
    "status": "published",
    "employment_type": "contract",
    "experience_level": "entry",
    "duration": "2 years renewable",
    "category": "UUID_HERE",
    "image_gallery": [
      "https://images.unsplash.com/photo-1584515933487-779824d29309",
      "https://images.unsplash.com/photo-1550831107-1553da8c8464"
    ]
  },
  {
    "title": "Registered Nurse – USA EB-3 Visa Program",
    "location": "Johns Hopkins Hospital",
    "remote": "on site",
    "country": "United States",
    "city": "Baltimore",
    "state": "Maryland",
    "description": "U.S. hospitals are seeking international Registered Nurses under the EB-3 visa sponsorship program. Includes family relocation support.",
    "status": "published",
    "employment_type": "full_time",
    "experience_level": "mid",
    "duration": "Permanent",
    "category": "UUID_HERE",
    "image_gallery": [
      "https://images.unsplash.com/photo-1629904853716-ece5d52f9c3e",
      "https://images.unsplash.com/photo-1606813902879-4b1e7b4b34b5"
    ]
  },
  {
    "title": "Dental Assistant – New Zealand Skilled Migration",
    "location": "Auckland Dental Centre",
    "remote": "on site",
    "country": "New Zealand",
    "city": "Auckland",
    "state": "",
    "description": "This opportunity is for qualified dental assistants looking to relocate to New Zealand under the skilled migrant visa program.",
    "status": "published",
    "employment_type": "full_time",
    "experience_level": "entry",
    "duration": "Permanent",
    "category": "UUID_HERE",
    "image_gallery": [
      "https://images.unsplash.com/photo-1606813902879-4b1e7b4b34b5",
      "https://images.unsplash.com/photo-1588776814546-1a85f7a66a2d"
    ]
  },
  {
    "title": "Elderly Caregiver – Japan Foreign Worker Program",
    "location": "Osaka Care Center",
    "remote": "on site",
    "country": "Japan",
    "city": "Osaka",
    "state": "",
    "description": "Work as a caregiver under Japan’s foreign skilled worker program. Includes Japanese language training and housing assistance.",
    "status": "published",
    "employment_type": "contract",
    "experience_level": "entry",
    "duration": "3 years renewable",
    "category": "UUID_HERE",
    "image_gallery": [
      "https://images.unsplash.com/photo-1505751172876-fa1923c5c528",
      "https://images.unsplash.com/photo-1576091160550-2173dba999ef"
    ]
  },
  {
    "title": "Radiology Technician – Australia Health Migration",
    "location": "Sydney Medical Imaging",
    "remote": "on site",
    "country": "Australia",
    "city": "Sydney",
    "state": "New South Wales",
    "description": "Join the Australian medical workforce as a certified Radiology Technician. Visa and relocation sponsorships available for eligible candidates.",
    "status": "published",
    "employment_type": "full_time",
    "experience_level": "mid",
    "duration": "4-year contract",
    "category": "UUID_HERE",
    "image_gallery": [
      "https://images.unsplash.com/photo-1576765607924-bd7ca748754d",
      "https://images.unsplash.com/photo-1629904853716-ece5d52f9c3e"
    ]
  },
  {
    "title": "Pharmacy Assistant – Ireland Health Program",
    "location": "Cork Community Hospital",
    "remote": "on site",
    "country": "Ireland",
    "city": "Cork",
    "state": "",
    "description": "Ireland’s healthcare recruitment drive seeks pharmacy assistants under full visa sponsorship and work training.",
    "status": "published",
    "employment_type": "full_time",
    "experience_level": "entry",
    "duration": "Permanent",
    "category": "UUID_HERE",
    "image_gallery": [
      "https://images.unsplash.com/photo-1612277795421-9b0fc9f94912",
      "https://images.unsplash.com/photo-1588776814546-1a85f7a66a2d"
    ]
  },
  {
    "title": "Public Health Officer – Sweden Global Talent Program",
    "location": "Karolinska University Hospital",
    "remote": "on site",
    "country": "Sweden",
    "city": "Stockholm",
    "state": "",
    "description": "Join Sweden’s Global Talent Health Program as a public health officer. This opportunity provides relocation, housing, and family support.",
    "status": "published",
    "employment_type": "contract",
    "experience_level": "senior",
    "duration": "3 years",
    "category": "UUID_HERE",
    "image_gallery": [
      "https://images.unsplash.com/photo-1550831107-1553da8c8464",
      "https://images.unsplash.com/photo-1584515933487-779824d29309"
    ]
  },
  {
    "title": "Healthcare Management Internship – Netherlands",
    "location": "Amsterdam Global Health Center",
    "remote": "hybrid",
    "country": "Netherlands",
    "city": "Amsterdam",
    "state": "",
    "description": "A paid internship for international students in healthcare administration. Includes visa sponsorship and housing assistance.",
    "status": "published",
    "employment_type": "internship",
    "experience_level": "student",
    "duration": "12 months",
    "category": "UUID_HERE",
    "image_gallery": [
      "https://images.unsplash.com/photo-1607746882042-944635dfe10e",
      "https://images.unsplash.com/photo-1584515933487-779824d29309"
    ]
  }
]


        for item in campaigns:
            category = category_map[item["category"]]
            campaign = Campaign.objects.create(
                title=item["title"],
                category=category,
                location=item["location"],
                remote=item["remote"],
                country=item["country"],
                city=item["city"],
                state=item["state"],
                description=item["description"],
                status=item["status"],
                employment_type=item["employment_type"],
                experience_level=item["experience_level"],
                duration=item["duration"],
            )

            if item["image_gallery"]:
                main_image_url = item["image_gallery"][0]
                img_temp = tempfile.NamedTemporaryFile(delete=True)
                img_temp.write(requests.get(main_image_url).content)
                img_temp.flush()
                campaign.image.save(
                    os.path.basename(main_image_url.split("?")[0]),
                    File(img_temp),
                    save=True,
                )

                for img_url in item["image_gallery"]:
                    temp_gallery = tempfile.NamedTemporaryFile(delete=True)
                    temp_gallery.write(requests.get(img_url).content)
                    temp_gallery.flush()
                    CampaignImages.objects.create(
                        canpaign=campaign,
                        image=File(temp_gallery, name=os.path.basename(img_url.split("?")[0])),
                    )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded campaigns with UUID categories"))
