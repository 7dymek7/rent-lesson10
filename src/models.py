"""Data models for the apartment management system.

This module defines all core data structures used throughout the system,
including apartments, tenants, transfers, bills, settlements, and events.
All models are implemented using Pydantic for validation and serialization.
"""

import json

from pydantic import BaseModel


class Parameters(BaseModel):
    """Configuration parameters for the apartment management system.

    Attributes:
        apartments_json_path (str): Path to the apartments JSON file.
        tenants_json_path (str): Path to the tenants JSON file.
        transfers_json_path (str): Path to the transfers JSON file.
        bills_json_path (str): Path to the bills JSON file.
        tenants_blacklist_json_path (str): Path to the tenant blacklist JSON file.
        apartment_events_json_path (str): Path to the apartment events JSON file.
        max_transfer_pln (float): Maximum allowed transfer amount.
        max_refund_pln (float): Maximum allowed refund amount (negative transfer).

    """

    apartments_json_path: str = "data/apartments.json"
    tenants_json_path: str = "data/tenants.json"
    transfers_json_path: str = "data/transfers.json"
    bills_json_path: str = "data/bills.json"
    tenants_blacklist_json_path: str = "data/tenants_blacklist.json"
    apartment_events_json_path: str = "data/apartment_events.json"

    max_transfer_pln: float = 4500.0
    max_refund_pln: float = 2500.0


class Room(BaseModel):
    """A room inside an apartment.

    Attributes:
        name (str): Name of the room.
        area_m2 (float): Area of the room in square meters.

    """

    name: str
    area_m2: float


class Apartment(BaseModel):
    """Represents an apartment with its metadata and rooms.

    Attributes:
        key (str): Unique identifier of the apartment.
        name (str): Human-readable apartment name.
        location (str): Address or location description.
        area_m2 (float): Total area of the apartment.
        rooms (dict[str, Room]): Mapping of room names to Room objects.

    """

    key: str
    name: str
    location: str
    area_m2: float
    rooms: dict[str, Room]

    @staticmethod
    def from_json_file(file_path: str) -> dict[str, "Apartment"]:
        """Load apartments from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            dict[str, Apartment]: Dictionary of apartment objects indexed by key.

        Raises:
            AssertionError: If the JSON structure is not a dictionary.

        """
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)

        assert isinstance(data, dict), "Expected a dictionary of apartments"
        return {key: Apartment(**apartment) for key, apartment in data.items()}


class Tenant(BaseModel):
    """Represents a tenant living in an apartment.

    Attributes:
        name (str): Full name of the tenant.
        apartment (str): Apartment key where the tenant lives.
        room (str): Room name assigned to the tenant.
        rent_pln (float): Monthly rent amount.
        deposit_pln (float): Deposit amount paid by the tenant.
        date_agreement_from (str): Start date of the rental agreement (YYYY-MM-DD).
        date_agreement_to (str): End date of the rental agreement (YYYY-MM-DD).

    """

    name: str
    apartment: str
    room: str
    rent_pln: float
    deposit_pln: float
    date_agreement_from: str
    date_agreement_to: str

    @staticmethod
    def from_json_file(file_path: str) -> dict[str, "Tenant"]:
        """Load tenants from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            dict[str, Tenant]: Dictionary of tenants indexed by tenant ID.

        Raises:
            AssertionError: If the JSON structure is not a dictionary.

        """
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)

        assert isinstance(data, dict), "Expected a dictionary of tenants"
        return {key: Tenant(**tenant) for key, tenant in data.items()}


class TenantBlacklistEntry(BaseModel):
    """Represents a blacklist entry for a tenant.

    Attributes:
        tenant (str): Name of the tenant.
        reason (str): Reason for blacklisting.

    """

    tenant: str
    reason: str

    @staticmethod
    def from_json_file(file_path: str) -> list["TenantBlacklistEntry"]:
        """Load tenant blacklist entries from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            list[TenantBlacklistEntry]: List of blacklist entries.

        Raises:
            AssertionError: If the JSON structure is not a list.

        """
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)

        assert isinstance(data, list), "Expected a list of blacklist entries"
        return [TenantBlacklistEntry(**entry) for entry in data]


class Transfer(BaseModel):
    """Represents a financial transfer made by a tenant.

    Attributes:
        amount_pln (float): Amount of the transfer.
        date (str): Date of the transfer (YYYY-MM-DD).
        settlement_year (int | None): Year the transfer applies to.
        settlement_month (int | None): Month the transfer applies to.
        tenant (str): Tenant identifier.
        type (str | None): Type of transfer (e.g., "rent", "deposit").

    """

    amount_pln: float
    date: str
    settlement_year: int | None
    settlement_month: int | None
    tenant: str
    type: str | None = None

    @staticmethod
    def from_json_file(file_path: str) -> list["Transfer"]:
        """Load transfers from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            list[Transfer]: List of transfer objects.

        Raises:
            AssertionError: If the JSON structure is not a list.

        """
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)

        assert isinstance(data, list), "Expected a list of transfers"
        return [Transfer(**transfer) for transfer in data]


class Bill(BaseModel):
    """Represents a bill issued for an apartment.

    Attributes:
        amount_pln (float): Amount of the bill.
        date_due (str): Due date of the bill (YYYY-MM-DD).
        apartment (str): Apartment key the bill applies to.
        settlement_year (int): Year the bill applies to.
        settlement_month (int): Month the bill applies to.
        type (str): Type of bill (e.g., "electricity", "water").

    """

    amount_pln: float
    date_due: str
    apartment: str
    settlement_year: int
    settlement_month: int
    type: str

    @staticmethod
    def from_json_file(file_path: str) -> list["Bill"]:
        """Load bills from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            list[Bill]: List of bill objects.

        Raises:
            AssertionError: If the JSON structure is not a list.

        """
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)

        assert isinstance(data, list), "Expected a list of bills"
        return [Bill(**bill) for bill in data]


class ApartmentSettlement(BaseModel):
    """Represents a monthly settlement summary for an apartment.

    Attributes:
        key (str): Unique settlement identifier.
        apartment (str): Apartment key.
        month (int): Settlement month.
        year (int): Settlement year.
        total_due_pln (float): Total amount due for the apartment.
        total_transfers_pln (float): Total transfers received.
        balance_pln (float): Remaining balance (positive = overpayment).

    """

    key: str
    apartment: str
    month: int
    year: int
    total_due_pln: float
    total_transfers_pln: float = 0.0
    balance_pln: float = 0.0


class TenantSettlement(BaseModel):
    """Represents a monthly settlement summary for a tenant.

    Attributes:
        tenant (str): Tenant name.
        apartment_settlement (str): Settlement key of the apartment.
        month (int): Settlement month.
        year (int): Settlement year.
        total_due_pln (float): Amount due from the tenant.
        total_transfers_pln (float): Transfers made by the tenant.
        balance_pln (float): Remaining balance.

    """

    tenant: str
    apartment_settlement: str
    month: int
    year: int
    total_due_pln: float
    total_transfers_pln: float = 0.0
    balance_pln: float = 0.0


class ApartmentEvent(BaseModel):
    """Represents an event or issue related to an apartment.

    Attributes:
        date (str): Date of the event (YYYY-MM-DD).
        apartment (str): Apartment key.
        amount_pln (float | None): Optional cost associated with the event.
        tenant (str | None): Tenant involved in the event, if any.
        description (str): Description of the event.
        solved (bool): Whether the event has been resolved.

    """

    date: str
    apartment: str
    amount_pln: float | None = None
    tenant: str | None = None
    description: str
    solved: bool = False

    @staticmethod
    def from_json_file(file_path: str) -> list["ApartmentEvent"]:
        """Load apartment events from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            list[ApartmentEvent]: List of apartment events.

        Raises:
            AssertionError: If the JSON structure is not a list.

        """
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)

        assert isinstance(data, list), "Expected a list of apartment events"
        return [ApartmentEvent(**event) for event in data]
