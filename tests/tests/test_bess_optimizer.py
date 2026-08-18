"""Automated Pytest Suite for BESS Engine."""

import pytest
from src.bess_optimizer import BESSEngine


def test_bess_initialization():
  engine = BESSEngine(capacity_mwh=20.0, power_mw=10.0)
  assert engine.capacity_mwh == 20.0
  assert engine.power_mw == 10.0
  assert engine.rte == 0.88


def test_positive_arbitrage_spread():
  engine = BESSEngine()
  margin = engine.calculate_arbitrage_spread(buy_price=20.0, sell_price=100.0)
  assert margin > 0
  assert margin == 54.77


def test_negative_spread_hurdle():
  engine = BESSEngine()
  margin = engine.calculate_arbitrage_spread(buy_price=50.0, sell_price=60.0)
  assert margin < 0


def test_invalid_timeseries_length():
  engine = BESSEngine()
  with pytest.raises(ValueError):
    engine.simulate_daily_dispatch([10.0, 20.0, 30.0])
