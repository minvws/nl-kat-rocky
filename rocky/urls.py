from django.urls import path, include
from django.contrib import admin
from two_factor.urls import urlpatterns as tf_urls
from django.views.generic.base import TemplateView
from django.conf.urls.i18n import i18n_patterns
from rocky import views

handler404 = "rocky.views.handler404"

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("onboarding/", include("onboarding.urls"), name="onboarding"),
    path("crisis-room/", include("crisis_room.urls"), name="crisis_room"),
    path("", views.LandingPageView.as_view(), name="landing_page"),
    path("account/", include("account.urls"), name="account"),
    path("organizations/", include("organizations.urls"), name="organizations"),
    path("kat-alogus/", include("katalogus.urls"), name="katalogus"),
    path("findings/", include("findings.urls"), name="findings"),
    path("objects/", include("oois.urls"), name=""),
    path("health/", views.health, name="health"),
    path(
        "health/v1/",
        views.HealthChecks.as_view(),
        name="health_beautified",
    ),
    path(
        "privacy-statement/",
        views.PrivacyStatementView.as_view(),
        name="privacy_statement",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("", include(tf_urls)),
)
