from django.urls import path, include
from findings import views

urlpatterns = [
    path("", views.FindingListView.as_view(), name="finding_list"),
    path("findings/add/", views.FindingAddView.as_view(), name="finding_add"),
    path("finding_type/add/", views.FindingTypeAddView.as_view(), name="finding_type_add"),
]
