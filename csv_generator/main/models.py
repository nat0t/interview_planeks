from django.db import models
from django.urls import reverse


class Schema(models.Model):
    COMMA = 'CM'
    TAB = 'TB'
    SPACE = 'SP'
    COLON = 'CL'
    SEMICOLON = 'SC'
    DELIMITERS = (
        (COMMA, 'Comma (,)'),
        (TAB, 'Tabulation ( )'),
        (SPACE, 'Space ( )'),
        (COLON, 'Colon (:)'),
        (SEMICOLON, 'Semicolon (;)'),
    )

    QUOTE = 'QT'
    DOUBLE_QUOTE = 'DQ'
    QUOTES = (
        (QUOTE, 'Quote (\')'),
        (DOUBLE_QUOTE, 'Double-quote (")'),
    )
    name = models.CharField(max_length=30, unique=True)
    delimiter = models.CharField(max_length=2, choices=DELIMITERS, default=COMMA)
    quotes = models.CharField(max_length=2, choices=QUOTES, default=DOUBLE_QUOTE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('main:list_schemas')


class SchemaDetails(models.Model):
    FULL_NAME = 'FN'
    JOB = 'JB'
    EMAIL = 'EM'
    PHONE_NUMBER = 'PN'
    DATE = 'DT'
    TYPES = (
        (FULL_NAME, 'Full name'),
        (JOB, 'Job'),
        (EMAIL, 'E-mail'),
        (PHONE_NUMBER, 'Phone number'),
        (DATE, 'Date'),
    )
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=2, choices=TYPES, default=None, blank=False)
    order = models.PositiveSmallIntegerField()
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)


class Dataset(models.Model):
    file = models.FileField(upload_to='', blank=True)
    task_id = models.CharField(max_length=50)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
