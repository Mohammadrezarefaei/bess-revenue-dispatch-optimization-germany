"""BESS Optimization & Degradation Engine."""

import numpy as np


class BESSEngine:

  def __init__(
      self,
      capacity_mwh: float = 20.0,
      power_mw: float = 10.0,
      rte: float = 0.88,
      deg_cost_eur_mwh: float = 22.50,
  ):
    self.capacity_mwh = capacity_mwh
    self.power_mw = power_mw
    self.rte = rte
    self.deg_cost = deg_cost_eur_mwh

  def calculate_arbitrage_spread(
      self, buy_price: float, sell_price: float
  ) -> float:
    """Calculates effective round-trip margin after efficiency loss and degradation hurdle."""
    effective_cost = (buy_price / self.rte) + self.deg_cost
    margin = sell_price - effective_cost
    return round(margin, 2)

  def simulate_daily_dispatch(
      self, spot_prices: list[float]
  ) -> dict[str, float]:
    """24h peak-valley dispatch simulation."""
    if len(spot_prices) != 24:
      raise ValueError('Spot prices must contain exactly 24 hourly values.')

    prices = np.array(spot_prices)
    min_idx = int(np.argmin(prices))
    max_idx = int(np.argmax(prices))

    buy_p = float(prices[min_idx])
    sell_p = float(prices[max_idx])
    margin = self.calculate_arbitrage_spread(buy_p, sell_p)

    if margin > 0:
      energy_dispatched = min(
          self.capacity_mwh * 0.9, self.power_mw * 2
      )  # 2-hour limit
      daily_profit = margin * energy_dispatched
    else:
      energy_dispatched = 0.0
      daily_profit = 0.0

    return {
        'buy_price': buy_p,
        'sell_price': sell_p,
        'net_margin_eur_mwh': margin,
        'energy_mwh': energy_dispatched,
        'daily_profit_eur': round(daily_profit, 2),
    }
