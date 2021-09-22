from django.db import models
from django.urls import reverse, reverse_lazy
from model_utils.models import TimeStampedModel
from django.utils.text import slugify

# Create your models here.
class School(TimeStampedModel):
    """[summary]

    Args:
        TimeStampedModel ([type]): [description]

    Returns:
        [type]: [description]
    """
    name = models.CharField(max_length=400)
    suffix = models.CharField(max_length=400)
    short = models.CharField(max_length=400)
    full = models.CharField(max_length=400)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(School, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    class Meta:
            ordering = ('-name',)

class Queue(TimeStampedModel):
    name = models.CharField(max_length=400)
    lh3id = models.PositiveIntegerField()
    queue_type = models.CharField(max_length=200)
    show = models.CharField(max_length=200)
    status = models.CharField(max_length=200, blank=True)
    avatar_link = models.CharField(max_length=1000)
    transcript_type = models.BooleanField()
    email = models.EmailField(max_length=400)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Queue, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
            ordering = ('-name',)
            
class Operator(TimeStampedModel):
    username = models.CharField(max_length=400)
    lh3operator_id =  models.IntegerField()
    show = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super(Operator, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    """
    def __repr__(self):
        return '\nid\t\t:{}\nslug\t\t:{}\nshortdesc\t:{}\n'.format(
            self.id, self.slug, self.shortdesc[:5]
            )
    """

    class Meta:
            ordering = ('-username',)

class Chat(TimeStampedModel):
    lh3id = models.PositiveIntegerField(unique=True)
    accepted = models.DateTimeField(blank=True, null=True)
    duration =  models.IntegerField(blank=True, null=True)
    guest =  models.CharField(max_length=800)
    ip =  models.CharField(max_length=300,blank=True, null=True) #To_delete
    operator = models.ForeignKey(Operator,blank=True, null=True, on_delete=models.CASCADE)
    profile =  models.CharField(max_length=300, blank=True, null=True)
    protocol =  models.CharField(max_length=100, blank=True)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    referrer = models.CharField(max_length=1500, blank=True, null=True)
    started = models.DateTimeField(blank=True, null=True)
    hour_started = models.IntegerField(blank=True, null=True) #To_delete
    ended = models.DateTimeField(blank=True, null=True)
    tags =  models.CharField(max_length=1000, blank=True) #To_delete
    wait = models.IntegerField(blank=True, null=True)  
    hasReferenceQuestion = models.IntegerField(blank=True, null=True, default=False)  


    def __str__(self):
        return self.guest

    #def get_absolute_url(self):
    #    return reverse('chat_edit', kwargs={'pk': self.pk})

    class Meta:
            ordering = ('-lh3id',)
            unique_together = (("guest","started", "lh3id"),)
            indexes = [
            models.Index(fields=['guest']),
        ]


class Transcript(TimeStampedModel):
    message = models.TextField(blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    referenceQuestion = models.BooleanField(blank=True, null=True, default=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, blank=True, null=True)
    chat_date = models.DateTimeField(blank=True, null=True)
    counter =  models.PositiveIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return str(self.id)

    #def get_absolute_url(self):
    #    return reverse('transcript_detail', kwargs={'pk': self.pk})

    class Meta:
            ordering = ('-id',)
            indexes = [
            models.Index(fields=['referenceQuestion']),
        ]

class TranscriptReview(TimeStampedModel):

    #faculty
    health = models.BooleanField(blank=True, null=True, default=False)
    business = models.BooleanField(blank=True, null=True, default=False)
    social_science = models.BooleanField(blank=True, null=True, default=False)
    law = models.BooleanField(blank=True, null=True, default=False)
    engineering = models.BooleanField(blank=True, null=True, default=False)

    #Reference questions   
    directional = models.BooleanField(blank=True, null=True, default=False)
    ready_reference = models.BooleanField(blank=True, null=True, default=False)
    in_depth = models.BooleanField(blank=True, null=True, default=False)
    technology = models.BooleanField(blank=True, null=True, default=False)
    citation = models.BooleanField(blank=True, null=True, default=False)

    #RUSA
    approachability = models.BooleanField(blank=True, null=True, default=False)
    interest = models.BooleanField(blank=True, null=True, default=False)
    listening = models.BooleanField(blank=True, null=True, default=False)
    searching = models.BooleanField(blank=True, null=True, default=False)

    #Review
    follow_up =  models.BooleanField(blank=True, null=True, default=False)
    training = models.BooleanField(blank=True, null=True, default=False)
    is_reviewed = models.BooleanField(blank=True, null=True, default=False)
    unanswered = models.BooleanField(blank=True, null=True, default=False)
    thank_you_note = models.BooleanField(blank=True, null=True, default=False)

    #Database Relationship
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, blank=True, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=True, null=True)
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE, blank=True, null=True)
    #https://core.ac.uk/download/pdf/215386429.pdf

    def __str__(self):
        return str(self.operator)

    class Meta:
            ordering = ('-id',)