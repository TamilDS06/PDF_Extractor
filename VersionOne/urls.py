from django.urls import path
from VersionOne.API.pdf_reader_api import ExtractPdf

urlpatterns = [
    path('et-pdf', ExtractPdf.as_view(), name = 'Extract_PDF_Details'),
]