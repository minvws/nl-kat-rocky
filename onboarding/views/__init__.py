from onboarding.views.base import CompleteOnboarding
from onboarding.views.introduction import index, OnboardingIntroductionView
from onboarding.views.choose_report import OnboardingChooseReportInfoView, OnboardingChooseReportTypeView
from onboarding.views.dns_report import DnsReportView
from onboarding.views.generate_report import OnboardingReportView
from onboarding.views.ooi_add import OnboardingSetupScanOOIAddView
from onboarding.views.ooi_detail import OnboardingSetupScanOOIDetailView
from onboarding.views.ooi_info import OnboardingSetupScanOOIInfoView
from onboarding.views.select_plugins import OnboardingSetupScanSelectPluginsView
from onboarding.views.set_clearance_level import OnboardingSetClearanceLevelView

# account setup views
from onboarding.views.account.account_setup_intro import OnboardingAccountSetupIntroView
from onboarding.views.account.account_user_type import OnboardingChooseUserTypeView
from onboarding.views.account.admin_add import OnboardingAccountSetupAdminView
from onboarding.views.account.client_add import OnboardingAccountSetupClientView
from onboarding.views.account.idemnification_setup import OnboardingIndemnificationSetupView
from onboarding.views.account.organization_edit import OnboardingOrganizationUpdateView
from onboarding.views.account.organization_setup import OnboardingOrganizationSetupView
from onboarding.views.account.redteamer_add import OnboardingAccountSetupRedTeamerView
from onboarding.views.account.registration_intro import OnboardingIntroductionRegistrationView


__all__ = [
    "CompleteOnboarding",
    "index",
    "OnboardingIntroductionView",
    "OnboardingChooseReportInfoView",
    "OnboardingChooseReportTypeView",
    "DnsReportView",
    "OnboardingReportView",
    "OnboardingSetupScanOOIAddView",
    "OnboardingSetupScanOOIDetailView",
    "OnboardingSetupScanOOIInfoView",
    "OnboardingSetupScanSelectPluginsView",
    "OnboardingSetClearanceLevelView",
    "OnboardingAccountSetupIntroView",
    "OnboardingChooseUserTypeView",
    "OnboardingAccountSetupAdminView",
    "OnboardingAccountSetupClientView",
    "OnboardingIndemnificationSetupView",
    "OnboardingOrganizationUpdateView",
    "OnboardingOrganizationSetupView",
    "OnboardingAccountSetupRedTeamerView",
    "OnboardingIntroductionRegistrationView",
]
