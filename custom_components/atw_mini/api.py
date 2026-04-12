"""API client for ATW MINI heat pumps."""

from __future__ import annotations

from aiohttp import BasicAuth, ClientError, ClientSession

from .const import DEFAULT_TIMEOUT
from .parser import (
    AtwMiniParseError,
    AtwMiniStatus,
    merge_status_data,
    parse_control_xml,
    parse_status_xml,
)


class AtwMiniApiError(Exception):
    """Base API error."""


class AtwMiniApiConnectionError(AtwMiniApiError):
    """Raised when the device cannot be reached."""


class AtwMiniApiParseError(AtwMiniApiError):
    """Raised when the response cannot be parsed."""


class AtwMiniApiClient:
    """Minimal async client for the heat pump XML endpoint."""

    def __init__(
        self,
        session: ClientSession,
        host: str,
        username: str,
        password: str,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self._session = session
        self._host = host.strip().rstrip("/")
        self._username = username
        self._password = password
        self._timeout = timeout

    @property
    def status_url(self) -> str:
        """Return the device status endpoint."""
        return f"http://{self._host}/status.xml"

    @property
    def control_url(self) -> str:
        """Return the device control endpoint."""
        return f"http://{self._host}/control.xml"

    async def async_get_status(self) -> AtwMiniStatus:
        """Fetch and parse device XML endpoints."""
        try:
            status_payload = await self._async_fetch_xml(self.status_url)
            control_payload = await self._async_fetch_xml(self.control_url)
        except ClientError as err:
            raise AtwMiniApiConnectionError("Unable to fetch device XML") from err

        try:
            status_text = status_payload.decode("windows-1250", errors="replace")
            control_text = control_payload.decode("windows-1250", errors="replace")
            return merge_status_data(
                parse_status_xml(status_text),
                parse_control_xml(control_text),
            )
        except UnicodeDecodeError as err:
            raise AtwMiniApiParseError("Unable to decode device response") from err
        except AtwMiniParseError as err:
            raise AtwMiniApiParseError(str(err)) from err

    async def _async_fetch_xml(self, url: str) -> bytes:
        """Fetch one XML endpoint."""
        async with self._session.get(
            url,
            auth=BasicAuth(self._username, self._password),
            timeout=self._timeout,
        ) as response:
            response.raise_for_status()
            return await response.read()
