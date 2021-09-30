from django.db import models
from django.urls import reverse, reverse_lazy
from model_utils.models import TimeStampedModel
from model_utils import Choices

class chatReferenceQuestion(TimeStampedModel):

    lh3ChatID = models.PositiveIntegerField(blank=True, null=True)
    ref_question_found = models.BooleanField(blank=True, null=True, default=False)
    ref_question_position = models.PositiveIntegerField( blank=True, null=True)
    operatorID = models.PositiveIntegerField( blank=True, null=True)
    queueID = models.PositiveIntegerField( blank=True, null=True)
    school =  models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.lh3ChatID

    def get_absolute_url(self):
        return reverse('chat_ref_edit', kwargs={'pk': self.pk})

    class Meta:
            ordering = ('-lh3ChatID',)
            indexes = [
            models.Index(fields=['lh3ChatID', 'queueID' ]),
        ]

class ChatLightAssessment(TimeStampedModel):

    STATUS = Choices(
        ('Canned Message', ('Canned Message')),
        ('Library Account', ('Library Account')),
        ('LibraryH3lp', ('LibraryH3lp')),
        ('Library Website Issue', ('Library Website Issue')),
    )
    
    status = models.CharField(
        max_length=32,
        choices=STATUS,
    )

    lh3ChatID = models.PositiveIntegerField(blank=True, null=True)
    to_follow_up = models.BooleanField(blank=True, null=True, default=False)
    comment =  models.CharField(max_length=300, blank=True, null=True)
    operatorID = models.PositiveIntegerField( blank=True, null=True)
    queueID = models.PositiveIntegerField( blank=True, null=True)
    school =  models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.lh3ChatID

    def get_absolute_url(self):
        return reverse('Chat_edit', kwargs={'pk': self.pk})

    class Meta:
            ordering = ('-lh3ChatID',)
            indexes = [
            models.Index(fields=['lh3ChatID', 'queueID' ]),
        ]