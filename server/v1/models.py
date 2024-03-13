from django.db import models


class EmailMessage(models.Model):
    type = models.CharField(max_length=32)
    subject = models.CharField(max_length=64)
    message = models.TextField()

    class Meta:
        verbose_name = 'почтовое_сообщение'
        verbose_name_plural = 'почтовые_сообщения'

    def __str__(self) -> str:
        return self.Meta.verbose_name
