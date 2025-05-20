from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=200, db_index=True)
    last_name = models.CharField(max_length=200, db_index=True)
    fullname = models.CharField(max_length=200, blank=True, null=True)
    personalEmail = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    personalPhone = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=200, blank=True, null=True)
    photoURL = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=200, blank=True, null=True)
    ethnicity = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    party = models.CharField(max_length=200, blank="U", null=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.CharField(max_length=200, blank=True, null=True)
    youtube = models.CharField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    parish = models.CharField(max_length=200, blank=True, null=True, db_index=True)

    def __str__(self):
        return self.fullname

    class Meta:
        abstract = True


class User(Person):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True, db_index=True)
    api_key = models.CharField(max_length=200, blank=True, null=True)


class Legislator(Person):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now=True, editable=True, db_index=True)
    chamber = models.CharField(max_length=200, db_index=True)
    districtnumber = models.IntegerField(default=0, db_index=True)
    officeaddress = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    officePhone = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    officeEmail = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    officeURL = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    officeTitle = models.CharField(max_length=200, blank=True, null=True, db_index=True)

    def __str__(self):
        return self.fullname

    def todict(self):
        return {
            "office_title": self.officeTitle,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.officeEmail,
            "personal_phone": self.personalPhone,
            "office_phone": self.officePhone,
            "office_url": self.officeURL,
            "district": self.districtnumber,
            "party": self.party,
            "gender": self.gender,
            "twitter": self.twitter,
            "facebook": self.facebook,
            "instagram": self.instagram,
            "campaign_url": "",
            "youtube": self.youtube,
            "chamber": self.chamber,
            "id": self.id,
        }


class API(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class Sheriff(Person):
#     parish = models.CharField(max_length=200)
#     department = models.CharField(max_length=200)
#     badge = models.CharField(max_length=200)
#     jurisdiction = models.CharField(max_length=200)
#     rank = models.CharField(max_length=200)
#
#
# class Chamber(models.Model):
#     name = models.CharField(max_length=200)
#
#
# class Council(Person):
#     name = models.CharField(max_length=200)
#     parish = models.CharField(max_length=200)
#     district = models.IntegerField(default=0)
#     year = models.IntegerField(default=0)


class SoSElectedOfficial(Person):
    id = models.AutoField(primary_key=True)
    officeTitle = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    officeDescription = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    officeAddress1 = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    officeAddress2 = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    officeCity = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    officeZip = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    officePhone = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    officeEmail = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    officeURL = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    mailForm = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    candidateAddress1 = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    candidateAddress2 = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    candidateCity = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    candidateZip = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    commissionedDate = models.DateTimeField(
        editable=True, db_index=True, blank=True, null=True
    )
    expirationDate = models.DateTimeField(
        editable=True, db_index=True, blank=True, null=True
    )
    officeLevel = models.IntegerField(default=0, db_index=True)
    candidateName = models.CharField(
        max_length=200, blank=True, null=True, db_index=True
    )
    city = models.CharField(max_length=200, blank=True, null=True, db_index=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def todict(self):
        return {
            "office_title": self.officeTitle,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.officeEmail,
            "mailform": self.mailForm,
            "office_phone": self.officePhone,
            "office_url": self.officeURL,
            "personal_phone": self.personalPhone,
            "website": self.website,
            "party": self.party,
            "gender": self.gender,
            "twitter": self.twitter,
            "facebook": self.facebook,
            "instagram": self.instagram,
            "campaign_url": "",
            "youtube": self.youtube,
            "city": self.city,
            "state": "LA",
            "id": self.id,
        }


class Request(models.Model):
    id = models.AutoField(primary_key=True)
    endpoint = models.CharField(max_length=100, null=True)  # The url the user requested
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )  # User that made request, if authenticated
    response_code = models.PositiveSmallIntegerField()  # Response status code
    method = models.CharField(max_length=10, null=True)  # Request method
    remote_address = models.CharField(max_length=20, null=True)  # IP address of user
    exec_time = models.IntegerField(null=True)  # Time taken to create the response
    date = models.DateTimeField(auto_now=True)  # Date and time of request
    body_response = models.TextField(blank=True)  # Response data
    body_request = models.TextField(blank=True)  # Request data
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    addressText = models.TextField(null=True, blank=True)
    referrer = models.TextField(null=True)
    user_agent = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"[{self.id}]: {self.remote_address} {self.method} {self.endpoint}"


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    endpoint = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    response_code = models.PositiveSmallIntegerField()
    method = models.CharField(max_length=10, null=True)
    remote_address = models.CharField(max_length=20, null=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    addressText = models.TextField(null=True, blank=True)
    referrer = models.TextField(null=True)
    official = models.ForeignKey(
        SoSElectedOfficial, on_delete=models.SET_NULL, null=True, blank=True
    )
    legislator = models.ForeignKey(
        Legislator, on_delete=models.SET_NULL, null=True, blank=True
    )
