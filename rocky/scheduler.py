import datetime
import json
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

import requests
from pydantic import BaseModel, Field

from rocky.health import ServiceHealth
from rocky.settings import SCHEDULER_API


class Boefje(BaseModel):
    """Boefje representation."""

    id: str
    name: Optional[str]
    description: Optional[str]
    repository_id: Optional[str]
    version: Optional[str] = Field(default=None)
    scan_level: Optional[int] = Field(default=None)
    consumes: Optional[Union[str, Set[str]]]
    produces: Optional[Set[str]]


class BoefjeMeta(BaseModel):
    """BoefjeMeta is the response object returned by the Bytes API"""

    id: str
    boefje: Boefje
    input_ooi: str
    arguments: Dict[str, Any]
    organization: str
    started_at: Optional[datetime.datetime]
    ended_at: Optional[datetime.datetime]


class RawData(BaseModel):
    id: Optional[str]
    boefje_meta: BoefjeMeta
    mime_types: List[Dict[str, str]]
    secure_hash: Optional[str]
    hash_retrieval_link: Optional[str]


class Normalizer(BaseModel):
    """Normalizer representation."""

    id: Optional[str]
    name: Optional[str]
    version: Optional[str] = Field(default=None)


class NormalizerTask(BaseModel):
    """NormalizerTask represent data needed for a Normalizer to run."""

    id: Optional[str]
    normalizer: Normalizer
    raw_data: RawData


class BoefjeTask(BaseModel):
    """BoefjeTask represent data needed for a Boefje to run."""

    id: Optional[str]
    boefje: Boefje
    input_ooi: str
    organization: str


class QueuePrioritizedItem(BaseModel):
    """Representation of a queue.PrioritizedItem on the priority queue. Used
    for unmarshalling of priority queue prioritized items to a JSON
    representation.
    """

    id: uuid.UUID
    priority: int
    hash: Optional[str]
    data: Union[BoefjeTask, NormalizerTask]


class TaskStatus(Enum):
    """Status of a task."""

    PENDING = "pending"
    QUEUED = "queued"
    DISPATCHED = "dispatched"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    id: str
    scheduler_id: str
    p_item: QueuePrioritizedItem
    status: TaskStatus
    created_at: datetime.datetime
    modified_at: datetime.datetime

    class Config:
        orm_mode = True


class PaginatedTasksResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[Task]


class SchedulerClient:
    def __init__(self, base_uri: str):
        self.session = requests.Session()
        self._base_uri = base_uri

    def list_tasks(
        self,
        queue_name: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[TaskStatus] = None,
        min_created_at: Optional[datetime.datetime] = None,
        max_created_at: Optional[datetime.datetime] = None,
        filters: Optional[List[Dict]] = None,
    ) -> PaginatedTasksResponse:
        params = {
            "scheduler_id": queue_name,
            "limit": limit,
            "offset": offset,
            "status": status,
            "min_created_at": min_created_at,
            "max_created_at": max_created_at,
        }

        res = self.session.get(f"{self._base_uri}/tasks", params=params, json=filters)
        return PaginatedTasksResponse.parse_raw(res.text)

    def get_task_details(self, task_id):
        res = self.session.get(f"{self._base_uri}/tasks/{task_id}")
        return res.json()

    def push_task(self, queue_name: str, prioritized_item: QueuePrioritizedItem) -> None:
        res = self.session.post(f"{self._base_uri}/queues/{queue_name}/push", data=prioritized_item.json())
        res.raise_for_status()

    def health(self) -> ServiceHealth:
        health_endpoint = self.session.get(f"{self._base_uri}/health")
        health_endpoint.raise_for_status()
        return ServiceHealth.parse_raw(health_endpoint.content)


client = SchedulerClient(SCHEDULER_API)
