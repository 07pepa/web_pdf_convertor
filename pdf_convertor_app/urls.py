from django.urls import path

from .views import status, rendered_page, upload

urlpatterns = [
    path('documents/', upload, name='document-upload'),
    path('documents/<uuid:doc_id>', status, name='document-status'),
    path('documents/<uuid:doc_id>/', status, name='document-status'),
    path('documents/<uuid:doc_id>/pages/<int:page_num>/', rendered_page, name='document-rendered-page'),
]
