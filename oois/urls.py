from django.urls import path
from oois.views import *

urlpatterns = [
    path("", OOIListView.as_view(), name="ooi_list"),
    path("graph/", OOIGraphView.as_view(), name="ooi_graph"),
    path("report/", OOIReportView.as_view(), name="ooi_report"),
    path("report/pdf/", OOIReportPDFView.as_view(), name="ooi_pdf_report"),
    path("summary/", OOISummaryView.as_view(), name="ooi_summary"),
    path("tree/", OOITreeView.as_view(), name="ooi_tree"),
    path("findings/", OOIFindingListView.as_view(), name="ooi_findings"),
    path("add/", OOIAddTypeSelectView.as_view(), name="ooi_add_type_select"),
    path(
        "objects/add-related/",
        OOIRelatedObjectAddView.as_view(),
        name="ooi_add_related",
    ),
    path("add/<ooi_type>/", OOIAddView.as_view(), name="ooi_add"),
    path("edit/", OOIEditView.as_view(), name="ooi_edit"),
    path("delete/", OOIDeleteView.as_view(), name="ooi_delete"),
    path("detail/", OOIDetailView.as_view(), name="ooi_detail"),
    path("export", OOIListExportView.as_view(), name="ooi_list_export"),
    path(
        "indemnification/reset/",
        ScanProfileResetView.as_view(),
        name="scan_profile_reset",
    ),
    path(
        "scan-profile/",
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
