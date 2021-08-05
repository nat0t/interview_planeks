from django.urls import path
from main.views import SchemaList, SchemaCreate, SchemaEdit, SchemaDelete, DatasetList, create_dataset

app_name = 'main'

urlpatterns = [
    path('list_schemas/', SchemaList.as_view(), name='list_schemas'),
    path('create_schema/', SchemaCreate.as_view(), name='create_schema'),
    path('edit_schema/<int:pk>/', SchemaEdit.as_view(), name='edit_schema'),
    path('delete_schema/<int:pk>/', SchemaDelete.as_view(), name='delete_schema'),
    path('list_datasets/<int:pk>/', DatasetList.as_view(), name='list_datasets'),
    path('create_dataset/', create_dataset, name='create_dataset'),
]
