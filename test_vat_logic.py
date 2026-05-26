"""
Unit tests for utils/vat_logic.py
Run with: pytest tests/test_vat_logic.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from utils.vat_logic import (
    calculate_vat_exclusive,
    calculate_vat_inclusive,
    check_registration_status,
    RegistrationStatus,
    KSA_VAT_RATE,
    MANDATORY_THRESHOLD,
    VOLUNTARY_THRESHOLD,
)


# ── VAT Exclusive ─────────────────────────────────────────────────────────────

class TestVATExclusive:
    def test_standard_amount(self):
        r = calculate_vat_exclusive(1000)
        assert r.subtotal == 1000.00
        assert r.vat_amount == 150.00
        assert r.total == 1150.00

    def test_zero_amount(self):
        r = calculate_vat_exclusive(0)
        assert r.vat_amount == 0
        assert r.total == 0

    def test_rate_pct_string(self):
        r = calculate_vat_exclusive(100)
        assert r.rate_pct == "15%"

    def test_rounding(self):
        r = calculate_vat_exclusive(333.33)
        assert r.vat_amount == round(333.33 * KSA_VAT_RATE, 2)
        assert r.total == round(333.33 + r.vat_amount, 2)


# ── VAT Inclusive ─────────────────────────────────────────────────────────────

class TestVATInclusive:
    def test_standard_amount(self):
        r = calculate_vat_inclusive(1150)
        assert r.subtotal == 1000.00
        assert r.vat_amount == 150.00
        assert r.total == 1150.00

    def test_roundtrip(self):
        """Exclusive output should match inclusive input."""
        excl = calculate_vat_exclusive(500)
        incl = calculate_vat_inclusive(excl.total)
        assert incl.subtotal == excl.subtotal
        assert incl.vat_amount == excl.vat_amount

    def test_zero_amount(self):
        r = calculate_vat_inclusive(0)
        assert r.subtotal == 0
        assert r.vat_amount == 0


# ── Registration Checker ──────────────────────────────────────────────────────

class TestRegistrationChecker:
    def test_mandatory_at_threshold(self):
        r = check_registration_status(MANDATORY_THRESHOLD)
        assert r.status == RegistrationStatus.MANDATORY

    def test_mandatory_above_threshold(self):
        r = check_registration_status(500_000)
        assert r.status == RegistrationStatus.MANDATORY

    def test_voluntary_at_lower_threshold(self):
        r = check_registration_status(VOLUNTARY_THRESHOLD)
        assert r.status == RegistrationStatus.VOLUNTARY

    def test_voluntary_in_range(self):
        r = check_registration_status(250_000)
        assert r.status == RegistrationStatus.VOLUNTARY

    def test_not_required_below_threshold(self):
        r = check_registration_status(100_000)
        assert r.status == RegistrationStatus.NOT_REQUIRED

    def test_not_required_at_zero(self):
        r = check_registration_status(0)
        assert r.status == RegistrationStatus.NOT_REQUIRED

    def test_just_below_mandatory(self):
        r = check_registration_status(MANDATORY_THRESHOLD - 1)
        assert r.status == RegistrationStatus.VOLUNTARY

    def test_just_below_voluntary(self):
        r = check_registration_status(VOLUNTARY_THRESHOLD - 1)
        assert r.status == RegistrationStatus.NOT_REQUIRED

    def test_result_has_explanation(self):
        r = check_registration_status(400_000)
        assert len(r.explanation) > 10
        assert len(r.action) > 10
