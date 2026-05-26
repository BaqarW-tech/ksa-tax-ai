"""
KSA VAT logic — pure calculation functions.
No Streamlit imports here; keeps logic testable in isolation.
"""

from dataclasses import dataclass
from enum import Enum

KSA_VAT_RATE = 0.15  # 15% standard rate

# ZATCA registration thresholds (SAR)
MANDATORY_THRESHOLD = 375_000
VOLUNTARY_THRESHOLD = 187_500


class RegistrationStatus(str, Enum):
    MANDATORY = "mandatory"
    VOLUNTARY = "voluntary"
    NOT_REQUIRED = "not_required"


@dataclass
class VATResult:
    """Result of a VAT calculation."""
    subtotal: float
    vat_amount: float
    total: float
    rate: float = KSA_VAT_RATE

    @property
    def rate_pct(self) -> str:
        return f"{self.rate * 100:.0f}%"


@dataclass
class RegistrationResult:
    """Result of a registration threshold check."""
    status: RegistrationStatus
    annual_revenue: float
    label: str
    explanation: str
    action: str


def calculate_vat_exclusive(amount: float) -> VATResult:
    """
    Amount is VAT-exclusive (VAT added on top).
    E.g. SAR 100 net → SAR 115 gross.
    """
    vat = round(amount * KSA_VAT_RATE, 2)
    return VATResult(
        subtotal=round(amount, 2),
        vat_amount=vat,
        total=round(amount + vat, 2),
    )


def calculate_vat_inclusive(amount: float) -> VATResult:
    """
    Amount already includes VAT (reverse VAT).
    E.g. SAR 115 gross → extract SAR 15 VAT, SAR 100 net.
    """
    subtotal = round(amount / (1 + KSA_VAT_RATE), 2)
    vat = round(amount - subtotal, 2)
    return VATResult(
        subtotal=subtotal,
        vat_amount=vat,
        total=round(amount, 2),
    )


def check_registration_status(annual_revenue: float) -> RegistrationResult:
    """
    Check VAT registration obligation based on annual taxable supplies.
    Thresholds per ZATCA VAT Implementing Regulations.
    """
    if annual_revenue >= MANDATORY_THRESHOLD:
        return RegistrationResult(
            status=RegistrationStatus.MANDATORY,
            annual_revenue=annual_revenue,
            label="Mandatory Registration Required",
            explanation=(
                f"Annual taxable supplies of SAR {annual_revenue:,.0f} exceed the mandatory "
                f"threshold of SAR {MANDATORY_THRESHOLD:,}. You must register for VAT with ZATCA."
            ),
            action="Register immediately at zatca.gov.sa to avoid penalties.",
        )
    elif annual_revenue >= VOLUNTARY_THRESHOLD:
        return RegistrationResult(
            status=RegistrationStatus.VOLUNTARY,
            annual_revenue=annual_revenue,
            label="Voluntary Registration Available",
            explanation=(
                f"Annual taxable supplies of SAR {annual_revenue:,.0f} fall between the voluntary "
                f"threshold (SAR {VOLUNTARY_THRESHOLD:,}) and mandatory threshold "
                f"(SAR {MANDATORY_THRESHOLD:,}). Registration is optional."
            ),
            action="Consider registering to reclaim input VAT on business expenses.",
        )
    else:
        return RegistrationResult(
            status=RegistrationStatus.NOT_REQUIRED,
            annual_revenue=annual_revenue,
            label="Registration Not Required",
            explanation=(
                f"Annual taxable supplies of SAR {annual_revenue:,.0f} are below the voluntary "
                f"threshold of SAR {VOLUNTARY_THRESHOLD:,}. No VAT registration is required."
            ),
            action="Monitor your revenue — register voluntarily if you want to reclaim input VAT.",
        )


def format_sar(amount: float) -> str:
    """Format a float as SAR currency string."""
    return f"SAR {amount:,.2f}"
