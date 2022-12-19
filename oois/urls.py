from django.urls import path, include
from oois.views import *

urlpatterns = [
    path("objects/graph/", OOIGraphView.as_view(), name="ooi_graph"),
    path("objects/report/", OOIReportView.as_view(), name="ooi_report"),
    path("objects/report/pdf/", OOIReportPDFView.as_view(), name="ooi_pdf_report"),
    path("objects/summary/", OOISummaryView.as_view(), name="ooi_summary"),
    path("objects/tree/", OOITreeView.as_view(), name="ooi_tree"),
    path("objects/findings/", OOIFindingListView.as_view(), name="ooi_findings"),
    path("objects/", OOIListView.as_view(), name="ooi_list"),
    path("objects/add/", OOIAddTypeSelectView.as_view(), name="ooi_add_type_select"),
    path(
        "objects/add-related/",
        OOIRelatedObjectAddView.as_view(),
        name="ooi_add_related",
    ),
    path("objects/add/<ooi_type>/", OOIAddView.as_view(), name="ooi_add"),
    path("objects/edit/", OOIEditView.as_view(), name="ooi_edit"),
    path("objects/delete/", OOIDeleteView.as_view(), name="ooi_delete"),
    path("objects/detail/", OOIDetailView.as_view(), name="ooi_detail"),
    path("objects/export", OOIListExportView.as_view(), name="ooi_list_export"),
    path(
        "objects/indemnification/reset/",
        ScanProfileResetView.as_view(),
        name="scan_profile_reset",
    ),
    path(
        "objects/scan-profile/",
        ScanProfileDetailView.as_view(),
        name="scan_profile_detail",
    ),
    path("scans/", ScanListView.as_view(), name="scan_list"),
    path(
        "upload/csv/",
        UploadCSV.as_view(),
        name="upload_csv",
    ),
]
