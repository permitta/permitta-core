from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StatusLabelsDto(BaseModel):
    id: str = Field()
    version: str | None = None


class StatusTrinoBundleMetricsDto(BaseModel):
    timer_bundle_request_ns: int = Field()
    timer_rego_load_bundles_ns: int = Field()
    timer_rego_module_compile_ns: int = Field()
    timer_rego_module_parse_ns: int = Field()


class StatusPlatformBundleDto(BaseModel):
    active_revision: Optional[str] = None
    last_request: Optional[datetime] = None
    last_successful_request: Optional[datetime] = None
    last_successful_download: Optional[datetime] = None
    last_successful_activation: Optional[datetime] = None
    metrics: Optional[StatusTrinoBundleMetricsDto] = None
    name: str = Field()
    size: int | None = None
    type: str | None = None


class StatusBundlesDto(BaseModel):
    trino: StatusPlatformBundleDto = Field()


class StatusDecisionLogsMetricsDto(BaseModel):
    counter_decision_logs_dropped: str = Field()
    decision_logs_nd_builtin_cache_dropped: str = Field()


class StatusDecisionLogsDto(BaseModel):
    code: str | None = Field(default=None)
    message: str | None = Field(default=None)
    http_code: str | None = Field(default=None)
    metrics: StatusDecisionLogsMetricsDto | None = Field(default=None)


class StatusDto(BaseModel):
    labels: StatusLabelsDto = Field()
    bundles: StatusBundlesDto | None = Field()
    decision_logs: StatusDecisionLogsDto | None = Field(default=None)
