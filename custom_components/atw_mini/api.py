"""API client for ATW MINI heat pumps."""

from __future__ import annotations

from aiohttp import BasicAuth, ClientError, ClientSession

from .const import DEFAULT_TIMEOUT
from .parser import AtwMiniParseError, AtwMiniStatus, parse_status_xml


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

    async def async_get_status(self) -> AtwMiniStatus:
        """Fetch and parse the XML device status."""
        try:
            async with self._session.get(
                self.status_url,
                auth=BasicAuth(self._username, self._password),
                timeout=self._timeout,
            ) as response:
                response.raise_for_status()
                payload = await response.read()
        except ClientError as err:
            raise AtwMiniApiConnectionError(f"Unable to fetch {self.status_url}") from err

        try:
            xml_text = payload.decode("windows-1250", errors="replace")
            return parse_status_xml(xml_text)
        except UnicodeDecodeError as err:
            raise AtwMiniApiParseError("Unable to decode device response") from err
        except AtwMiniParseError as err:
            raise AtwMiniApiParseError(str(err)) from err
