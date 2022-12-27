from django.urls import path
from onboarding import views


urlpatterns = [
    path("", views.index, name="onboarding_index"),
    path(
        "step/introduction/",
        views.OnboardingIntroductionView.as_view(),
        name="step_introduction",
    ),
    path(
        "step/choose-report-info/",
        views.OnboardingChooseReportInfoView.as_view(),
        name="step_choose_report_info",
    ),
    path(
        "step/choose-report-type/",
        views.OnboardingChooseReportTypeView.as_view(),
        name="step_choose_report_type",
    ),
    path(
        "step/setup-scan/ooi/info/",
        views.OnboardingSetupScanOOIInfoView.as_view(),
        name="step_setup_scan_ooi_info",
    ),
    path(
        "step/setup-scan/ooi/detail/",
        views.OnboardingSetupScanOOIDetailView.as_view(),
        name="step_setup_scan_ooi_detail",
    ),
    path(
        "step/set-clearance-level/",
        views.OnboardingSetClearanceLevelView.as_view(),
        name="step_set_clearance_level",
    ),
    path(
        "step/setup-scan/select-plugins/",
        views.OnboardingSetupScanSelectPluginsView.as_view(),
        name="step_setup_scan_select_plugins",
    ),
    path(
        "step/setup-scan/<ooi_type>/",
        views.OnboardingSetupScanOOIAddView.as_view(),
        name="step_setup_scan_ooi_add",
    ),
    path(
        "step/report/",
        views.OnboardingReportView.as_view(),
        name="step_report",
    ),
    path(
        "step/report/dns-report/",
        views.DnsReportView.as_view(),
        name="dns_report",
    ),
    path(
        "step/introduction/registration/",
        views.OnboardingIntroductionRegistrationView.as_view(),
        name="step_introduction_registration",
    ),
    path(
        "step/organization-setup/",
        views.OnboardingOrganizationSetupView.as_view(),
        name="step_organization_setup",
    ),
    path(
        "<organization_code>/step/organization-setup/update/",
        views.OnboardingOrganizationUpdateView.as_view(),
        name="step_organization_update",
    ),
    path(
        "<organization_code>/step/indemnification-setup/",
        views.OnboardingIndemnificationSetupView.as_view(),
        name="step_indemnification_setup",
    ),
    path(
        "step/choose-user-type/",
        views.OnboardingChooseUserTypeView.as_view(),
        name="step_choose_user_type",
    ),
    path(
        "<organization_code>/step/choose-user-type/",
        views.OnboardingChooseUserTypeView.as_view(),
        name="step_choose_user_type",
    ),
    path(
        "<organization_code>/step/complete-onboarding/",
        views.CompleteOnboarding.as_view(),
        name="complete_onboarding",
    ),
    path(
        "<organization_code>/step/account-setup/introduction/",
        views.OnboardingAccountSetupIntroView.as_view(),
        name="step_account_setup_intro",
    ),
    path(
        "<organization_code>/step/account-setup/admin/",
        views.OnboardingAccountSetupAdminView.as_view(),
        name="step_account_setup_admin",
    ),
    path(
        "<organization_code>/step/account-setup/red-teamer/",
        views.OnboardingAccountSetupRedTeamerView.as_view(),
        name="step_account_setup_red_teamer",
    ),
    path(
        "<organization_code>/step/account-setup/client/",
        views.OnboardingAccountSetupClientView.as_view(),
        name="step_account_setup_client",
    ),
]
