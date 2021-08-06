import csv
import os
import time
import boto3

from celery import shared_task
from faker import Faker

from csv_generator.settings import MEDIA_ROOT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET
from main.models import Schema, SchemaDetails, Dataset


@shared_task(bind=True)
def generate_data(self, schema_id, rows):
    filename = f'file_{schema_id}_{time.time()}.csv'
    Dataset.objects.create(schema=Schema.objects.get(id=schema_id), file=filename, task_id=self.request.id)

    schema_id = int(schema_id)
    rows = int(rows)
    schema_columns = SchemaDetails.objects.filter(schema=schema_id)
    columns = [(column.order, column.name, column.type) for column in schema_columns]
    columns.sort()
    names = [column[1] for column in columns]
    types = [column[2] for column in columns]

    delimiter_dict = {
        'CM': ',',
        'TB': '\t',
        'SP': ' ',
        'CL': ':',
        'SC': ';',
    }
    delimiter = delimiter_dict[Schema.objects.get(id=schema_id).delimiter]
    quotes_dict = {
        'QT': "'",
        'DQ': '"',
    }
    quotes = quotes_dict[Schema.objects.get(id=schema_id).quotes]

    filepath = os.path.join(MEDIA_ROOT, filename)
    fake = Faker()
    gen_template = {
        'FN': fake.name,
        'JB': fake.job,
        'EM': fake.email,
        'PN': fake.phone_number,
        'DT': fake.date,
    }
    with open(filepath, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotes)
        writer.writerow(names)
        for _ in range(rows):
            types_fake = [gen_template[item]() for item in types]
            writer.writerow(types_fake)

    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3_client.upload_file(filepath, S3_BUCKET, filename)
