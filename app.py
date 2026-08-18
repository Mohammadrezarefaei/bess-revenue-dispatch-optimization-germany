"""Interactive Streamlit Web Dashboard for Utility BESS Sizing & Revenue Optimization."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='Utility BESS Dispatch Simulator (Germany)',
    page_icon='🔋',
    layout='wide',
)

st.title('🔋 Utility BESS Techno-Economic Dispatch Optimizer')
st.markdown(
    'Interactive simulation model for **utility-scale Battery Energy Storage'
    ' Systems (BESS)** in the German **EPEX Spot / Day-Ahead** wholesale'
    ' electricity market.'
)

# Sidebar - Parameter Tuning
st.sidebar.header('⚙️ Technical & Economic Sizing')
power_mw = st.sidebar.slider(
    'Rated Power Capacity (MW)',
    min_value=1.0,
    max_value=50.0,
    value=10.0,
    step=1.0,
)
duration_h = st.sidebar.slider(
    'Storage Duration (Hours)',
    min_value=1.0,
    max_value=4.0,
    value=2.0,
    step=0.5,
)
capacity_mwh = power_mw * duration_h

rte = (
    st.sidebar.slider(
        'Round-Trip Efficiency RTE (%)',
        min_value=75,
        max_value=95,
        value=88,
        step=1,
    )
    / 100.0
)
deg_cost = st.sidebar.slider(
    'LFP Degradation Wear Cost (€/MWh)',
    min_value=10.0,
    max_value=40.0,
    value=22.50,
    step=0.5,
)
capex_per_kwh = st.sidebar.slider(
    'Turnkey Capex (€/kWh)', min_value=200, max_value=500, value=350, step=25
)

# 24-Hour Spot Market Profile Generator
hours = np.arange(24)
# Typical German merit-order profile (PV midday suppression + evening peak)
spot_prices = (
    55.0
    + 38.0 * np.sin((hours - 6) * np.pi / 12)
    - 28.0 * np.exp(-(((hours - 13) / 2.2) ** 2))
)

# Dispatch Logic
min_idx = int(np.argmin(spot_prices))
max_idx = int(np.argmax(spot_prices))
buy_p = spot_prices[min_idx]
sell_p = spot_prices[max_idx]

# Effective round-trip cost & hurdle margin
effective_charging_cost = (buy_p / rte) + deg_cost
net_margin = sell_p - effective_charging_cost

# Layout: 2 Columns
col1, col2 = st.columns([2, 1])

with col1:
  st.subheader('📊 24-Hour Day-Ahead Price Profile & Dispatch Schedule')
  fig, ax = plt.subplots(figsize=(10, 4.8))
  ax.plot(
      hours,
      spot_prices,
      marker='o',
      color='#2563EB',
      lw=2.2,
      label='EPEX Spot Wholesale Price (€/MWh)',
  )

  # Highlight charge and discharge windows
  ax.axvspan(
      min_idx - 0.4,
      min_idx + 0.4,
      color='#10B981',
      alpha=0.3,
      label=f'Optimal Charge Window (Hour {min_idx}: €{buy_p:.2f}/MWh)',
  )
  ax.axvspan(
      max_idx - 0.4,
      max_idx + 0.4,
      color='#EF4444',
      alpha=0.3,
      label=f'Optimal Discharge Window (Hour {max_idx}: €{sell_p:.2f}/MWh)',
  )

  ax.set_xlabel('Hour of Day [0 - 23h]', fontweight='bold')
  ax.set_ylabel('Day-Ahead Price [€/MWh]', fontweight='bold')
  ax.set_xticks(hours)
  ax.grid(True, linestyle=':', alpha=0.6)
  ax.legend(loc='upper left')
  st.pyplot(fig)

with col2:
  st.subheader('📈 Financial & Operating Metrics')
  st.metric(
      label='Configured Storage Asset',
      value=f'{capacity_mwh:.1f} MWh',
      delta=f'{power_mw:.0f} MW ({duration_h:.1f}h C-Rate)',
  )
  st.metric(
      label='Realized Arbitrage Margin',
      value=f'€{net_margin:.2f} / MWh',
      delta='Bankable Spread' if net_margin > 0 else 'Unbankable Spread',
  )

  # Annual Financial Projections
  annual_cycles = 330
  dispatched_energy_per_cycle = min(capacity_mwh * 0.9, power_mw * duration_h)
  annual_ebitda = max(
      0.0, net_margin * dispatched_energy_per_cycle * annual_cycles
  )
  total_capex = capacity_mwh * (capex_per_kwh * 1000.0)
  payback = total_capex / annual_ebitda if annual_ebitda > 0 else 99.0

  st.metric(
      label='Annualized Arbitrage EBITDA',
      value=f'€{annual_ebitda/1e3:,.1f} k / year',
  )
  st.metric(
      label='Simple Project Payback',
      value=f'{payback:.1f} Years' if payback < 50 else '> 50 Years',
  )

st.markdown('---')
st.markdown("""
**Methodology & Physics Notes:**
* **Degradation Hurdle:** Ensures battery cycling is restricted to high-spread market intervals, protecting LFP electrochemical cycle life.
* **RTE Formulation:** Accounts for round-trip power electronics and electrochemical conversion losses: $\text{Eff. Cost} = (P_{\text{charge}} / \eta_{\text{RTE}}) + C_{\text{deg}}$.
""")
