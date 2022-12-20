from typing import Type
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.urls.base import reverse
from django.contrib.auth.models import Group
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.views import View
from oois.views import BaseOOIDetailView
from oois.ooi_helpers import create_object_tree_item_from_ref, filter_ooi_tree
from onboarding.mixins import RedTeamUserRequiredMixin
from oois.views import Report, build_findings_list_from_store
from organizations.models import OrganizationMember
from organizations.mixins import OrganizationsMixin


class BaseReportView(RedTeamUserRequiredMixin, BaseOOIDetailView):
    report: Type[Report]
    depth = 15

    def get_tree_dict(self):
        return create_object_tree_item_from_ref(self.tree.root, self.tree.store)

    def get_filtered_tree(self, tree_dict):
        return filter_ooi_tree(tree_dict, self.report.get_ooi_type_filter())

    def get_findings_list(self):
        return build_findings_list_from_store(self.tree.store, self.report.get_finding_filter())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["findings_list"] = self.get_findings_list()
        context["tree"] = self.get_filtered_tree(self.get_tree_dict())
        return context


@class_view_decorator(otp_required)
class CompleteOnboarding(OrganizationsMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            redteam_group = Group.objects.get(name="redteam")
            redteam_group.user_set.add(request.user)
            member, _ = OrganizationMember.objects.get_or_create(user=request.user, organization=self.organization)
            member.onboarded = True
            member.save()
        else:
            member = OrganizationMember.objects.get(user=request.user, organization=self.organization)
            member.onboarded = True
            member.save()
        return redirect(reverse("crisis_room"))
