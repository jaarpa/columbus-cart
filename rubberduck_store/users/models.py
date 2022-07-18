from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import int_list_validator

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    age = models.PositiveIntegerField(_("Age"))
    MALE = "Male"
    FEMALE = "Female"
    OTHER_gender = "Non-binary"
    genderS = [
        (MALE, _("Male")),
        (FEMALE, _("Female")),
        (OTHER_gender, _("Non-binary")),
    ]
    gender = models.CharField(
        max_length=10, choices=genderS, null=False, blank=False
    )
    phone = models.CharField(
        _("Phone number"),
        validators=[int_list_validator(sep="")],
        max_length=10,
        null=False,
        blank=False,
    )
    seller = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"Profile: {self.user.username}"

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})
