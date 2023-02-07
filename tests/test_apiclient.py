"""Test sendafd.apiclient module"""

import pytest
import apiclient
from unittest import mock


def test_print_region_codes(capsys):
    apiclient.print_region_codes({"ABQ": "Albuquerque, NM", "ABR": "Aberdeen, SD"})
    captured = capsys.readouterr()
    assert "ABQ Albuquerque, NM\nABR Aberdeen, SD" in captured.out
