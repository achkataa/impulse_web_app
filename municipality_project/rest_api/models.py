from django.db import models

# Create your models here.

class UserNotification(models.Model):
    CREDENTIAL_SUBJECT_MAX_LENGTH=1000
    SESSION_ID_MAX_LENGTH=1000
    credential_subject = models.CharField(
        max_length=CREDENTIAL_SUBJECT_MAX_LENGTH
    )

    session_id = models.CharField(
        max_length=SESSION_ID_MAX_LENGTH
    )
