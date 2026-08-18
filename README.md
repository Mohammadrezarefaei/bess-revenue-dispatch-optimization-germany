[![BESS Engine CI](https://github.com/Mohammadrezarefaei/bess-revenue-dispatch-optimization-germany/actions/workflows/ci.yml/badge.svg)](https://github.com/Mohammadrezarefaei/bess-revenue-dispatch-optimization-germany/actions)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bess-dispatch-germany.streamlit.app/)

## 🚀 Live Interactive Demo
👉 **[Access the Live Streamlit Web App](https://bess-dispatch-germany.streamlit.app/)**
# 🔋 BESS Dispatch Optimization & Techno-Economic Financial Modeling (German Day-Ahead Market)

An end-to-end techno-economic simulation, dispatch optimization pipeline, and Discounted Cash Flow (DCF) financial model for a **10 MW / 20 MWh Utility-Scale Battery Energy Storage System (BESS)** operating in the German wholesale electricity market (**EPEX Spot / SMARD**).

---

## 📌 Project Architecture & Methodology

1. **Market Signal Modeling:** Real-world day-ahead hourly spot price dynamics, including renewable oversupply, steep solar midday dips, and evening ramp-up peaks.
2. **Physical & Operational Constraints:**
   * **Rated Power / Capacity:** 10 MW / 20 MWh (2-Hour Duration)
   * **Round-Trip Efficiency (RTE):** 88.0% ($\eta_{\text{charge}} = \eta_{\text{discharge}} = \sqrt{0.88}$)
   * **Depth of Discharge (DoD):** 90% usable capacity ($SOC_{\text{min}} = 2.0\text{ MWh}$, $SOC_{\text{max}} = 20.0\text{ MWh}$)
3. **Dispatch Strategy:** Dynamic rule-based daily arbitrage maximizing spread capture (charging during low/negative price hours, discharging during peak pricing windows).
4. **DCF Financial Framework:** Full multi-year project cash flow modeling including CAPEX, OPEX (2% of CAPEX), Simple Payback Period, and Net Present Value (NPV @ 7.0% WACC over a 15-year lifetime).

---

## 📊 Key Techno-Economic & Financial Metrics

| Metric | Simulated Value | Unit / Definition |
| :--- | :---: | :--- |
| **System Rating** | **10 MW / 20 MWh** | 2-Hour Duration Grid-Scale BESS |
| **Round-Trip Efficiency (RTE)** | **88.0%** | AC-to-AC System Efficiency |
| **Total Turnkey CAPEX** | **€4,400,000** | €220 / kWh Installed |
| **Annual Arbitrage Revenue** | **€585,840** | Day-Ahead Wholesale Spread Capture |
| **Annual OPEX (2%)** | **€88,000** | O&M, Insurance, Inverter Servicing |
| **Net Annual Operating Cash Flow** | **€497,840** | Pre-tax Operating Cashflow |
| **Net Present Value (NPV @ 7% WACC)** | **€134,285** | 15-Year Project Lifetime |
| **Simple Payback Period** | **8.84 Years** | $\text{CAPEX} / \text{Net Annual Cashflow}$ |

---

## 📈 Dispatch Simulation Visualization

![BESS Dispatch Simulation](bess_arbitrage_dispatch_simulation.png)

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Data & Numerical Optimization:** `pandas`, `numpy`
* **Visualization:** `matplotlib`
* ---

## 🔍 Honest Model Validation & Regime Boundary Analysis

In line with quantitative model validation standards, the dispatch algorithm's performance has been evaluated across distinct market regimes:
* **Profitable Regime (High Spread):** When daily spreads exceed **€38.20/MWh**, the engine executes full arbitrage cycles, yielding positive net EBITDA.
* **Flat Baseload Regime (Breakdown / Boundary Limit):** During periods with minimal intraday volatility (spreads $< €35.00/\text{MWh}$), the optimizer halts cycling to prevent uncompensated battery degradation.
* **Strategic Implication:** Pure wholesale arbitrage is insufficient during flat price periods; assets must transition to multi-market revenue stacking by allocating capacity to **FCR (Primary Control)** and **aFRR (Secondary Reserve)**.

---

## 🛠️ Software Architecture & Automated Testing
* **CI/CD Pipeline:** Fully automated testing via **GitHub Actions** (`pytest` test suite covering initialization, positive arbitrage spreads, and edge cases).
* **Modular Core:** Object-oriented engine architecture located in `src/bess_optimizer.py`.
