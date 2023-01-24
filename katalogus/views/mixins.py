from datetime import datetime, timezone
from logging import getLogger
from typing import List, Optional
from uuid import uuid4

from django.urls import reverse
from octopoes.connector.octopoes import OctopoesAPIConnector
from octopoes.models import OOI, DeclaredScanProfile

from katalogus.client import get_katalogus, Plugin
from rocky.scheduler import Boefje, BoefjeTask, QueuePrioritizedItem, client
from rocky.views.mixins import OctopoesMixin
from tools.models import Organization

logger = getLogger(__name__)


class KATalogusMixin:
    def setup(self, request, *args, **kwargs):
        """
        Prepare organization info and KAT-alogus API client.
        """
        super().setup(request, *args, **kwargs)
        if request.user.is_anonymous:
            return reverse("login")
        else:
            self.organization = request.user.organizationmember.organization
            self.katalogus_client = get_katalogus(self.organization.code)
            if "plugin_id" in kwargs:
                self.plugin_id = kwargs["plugin_id"]
                self.plugin = self.katalogus_client.get_plugin_details(self.plugin_id)
                self.plugin_schema = self.katalogus_client.get_plugin_schema(self.plugin_id)


class BoefjeMixin(OctopoesMixin):
    """
    When a user wants to scan one or multiple OOI's,
    this mixin provides the methods to construct the boefjes for the OOI's and run them.
    """

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.api_connector = self.get_api_connector()

    def run_boefje(self, katalogus_boefje: Plugin, ooi: Optional[OOI], organization: Organization) -> None:

        boefje_queue_name = f"boefje-{organization.code}"

        boefje = Boefje(
            id=katalogus_boefje.id,
            name=katalogus_boefje.name,
            description=katalogus_boefje.description,
            repository_id=katalogus_boefje.repository_id,
            version=None,
            scan_level=katalogus_boefje.scan_level.value,
            consumes={ooi_class.get_ooi_type() for ooi_class in katalogus_boefje.consumes},
            produces={ooi_class.get_ooi_type() for ooi_class in katalogus_boefje.produces},
        )

        boefje_task = BoefjeTask(
            id=uuid4().hex,
            boefje=boefje,
            input_ooi=ooi.reference if ooi else None,
            organization=organization.code,
        )

        item = QueuePrioritizedItem(id=boefje_task.id, priority=1, data=boefje_task)
        logger.info("Item: %s", item.json())
        client.push_task(boefje_queue_name, item)

    def run_boefje_for_oois(
        self,
        boefje: Plugin,
        oois: List[OOI],
        organization: Organization,
        api_connector: OctopoesAPIConnector,
    ) -> None:
        if not oois and not boefje.consumes:
            self.run_boefje(boefje, None, organization)

        for ooi in oois:

            if ooi.scan_profile.level < boefje.scan_level:
                api_connector.save_scan_profile(
                    DeclaredScanProfile(
                        reference=ooi.reference,
                        level=boefje.scan_level,
                    ),
                    datetime.now(timezone.utc),
                )
            self.run_boefje(boefje, ooi, organization)
