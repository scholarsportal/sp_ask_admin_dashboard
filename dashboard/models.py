from django.db import models
from django.urls import reverse, reverse_lazy


class ReferenceQuestion(models.Model):
    message = models.TextField(blank=True, null=True)
    is_anonymized = models.BooleanField(blank=True, null=True, default=False)
    lh3ChatID = models.PositiveIntegerField(blank=True, null=True)
    chat_date = models.DateTimeField(blank=True, null=True)
    reference_question_line_number = models.PositiveIntegerField(
        blank=True, null=True, default=0
    )

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("rq__detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("-id",)
        indexes = [
            models.Index(fields=["lh3ChatID"]),
        ]
