"""
Rebate Optimization Sandbox
Interactive Streamlit UI for optimizing trading strategy rebate parameters using Optuna
"""

import streamlit as st
import pandas as pd
import numpy as np
import optuna
from optuna.visualization import (
    plot_optimization_history,
    plot_param_importances,
    plot_parallel_coordinate
)
import plotly.graph_objects as go
from datetime import datetime, timedelta


# Configure Streamlit page
st.set_page_config(
    page_title="Rebate Optimization Sandbox",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Rebate Optimization Sandbox")
st.markdown("*Optimize trading rebate parameters using Optuna hyperparameter optimization*")


# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    optimization_mode = st.selectbox(
        "Optimization Mode",
        ["Single Rebate", "Multi-Asset Rebate", "Dynamic Rebate"]
    )

    n_trials = st.slider("Number of Trials", 10, 500, 100)

    st.divider()

    st.header("📈 Strategy Parameters")
    base_volume = st.number_input("Base Trading Volume ($)", 100000, 10000000, 1000000, 100000)
    trading_frequency = st.slider("Trading Frequency (trades/day)", 1, 100, 10)
    risk_tolerance = st.slider("Risk Tolerance", 0.0, 1.0, 0.5, 0.1)


# Simulate trading performance with rebates
def simulate_trading_performance(rebate_pct, maker_taker_ratio, volume, frequency):
    """
    Simulate trading performance with given rebate parameters

    Returns: Sharpe ratio (higher is better)
    """
    # Base returns simulation
    daily_returns = np.random.normal(0.001, 0.02, 252)

    # Transaction costs
    base_cost = 0.001  # 0.1% base transaction cost
    maker_rebate = rebate_pct / 100 * maker_taker_ratio
    taker_cost = base_cost * (1 - maker_taker_ratio)

    net_cost = taker_cost - maker_rebate

    # Apply costs based on trading frequency
    cost_drag = net_cost * frequency / 252
    adjusted_returns = daily_returns - cost_drag

    # Calculate Sharpe ratio
    sharpe = np.mean(adjusted_returns) / np.std(adjusted_returns) * np.sqrt(252)

    # Penalize for extreme parameters
    if rebate_pct > 5.0 or maker_taker_ratio > 0.9:
        sharpe *= 0.8

    return sharpe


# Optuna objective function
def objective(trial):
    """Optuna objective to maximize Sharpe ratio"""

    # Suggest parameters
    rebate_pct = trial.suggest_float("rebate_percentage", 0.0, 10.0)
    maker_taker_ratio = trial.suggest_float("maker_taker_ratio", 0.0, 1.0)
    position_size = trial.suggest_float("position_size_pct", 0.1, 1.0)

    # Simulate performance
    sharpe = simulate_trading_performance(
        rebate_pct,
        maker_taker_ratio,
        base_volume * position_size,
        trading_frequency
    )

    return sharpe


# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Optimization Results")

    if st.button("🚀 Run Optimization", type="primary"):
        with st.spinner(f"Running {n_trials} optimization trials..."):
            # Create and run Optuna study
            study = optuna.create_study(
                direction="maximize",
                sampler=optuna.samplers.TPESampler(seed=42)
            )

            study.optimize(objective, n_trials=n_trials, show_progress_bar=False)

            # Store in session state
            st.session_state.study = study
            st.session_state.best_params = study.best_params
            st.session_state.best_value = study.best_value

        st.success("Optimization complete!")

with col2:
    st.subheader("📊 Best Parameters")

    if "best_params" in st.session_state:
        params = st.session_state.best_params
        value = st.session_state.best_value

        st.metric("Best Sharpe Ratio", f"{value:.4f}")
        st.divider()

        st.metric("Optimal Rebate %", f"{params['rebate_percentage']:.2f}%")
        st.metric("Maker/Taker Ratio", f"{params['maker_taker_ratio']:.2%}")
        st.metric("Position Size", f"{params['position_size_pct']:.2%}")

        # Calculate estimated savings
        annual_savings = (
            params['rebate_percentage'] / 100 *
            base_volume *
            trading_frequency * 252 *
            params['maker_taker_ratio']
        )
        st.metric("Estimated Annual Savings", f"${annual_savings:,.0f}")


# Visualization tabs
if "study" in st.session_state:
    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Optimization History",
        "🎯 Parameter Importance",
        "🔀 Parallel Coordinates",
        "📊 Trial Data"
    ])

    study = st.session_state.study

    with tab1:
        st.plotly_chart(
            plot_optimization_history(study),
            use_container_width=True
        )
        st.caption("Shows how the objective value improves over trials")

    with tab2:
        try:
            st.plotly_chart(
                plot_param_importances(study),
                use_container_width=True
            )
            st.caption("Indicates which parameters have the most impact on performance")
        except:
            st.info("Parameter importance available after sufficient trials")

    with tab3:
        st.plotly_chart(
            plot_parallel_coordinate(study),
            use_container_width=True
        )
        st.caption("Visualizes relationships between parameters and objective value")

    with tab4:
        # Create trials dataframe
        trials_df = study.trials_dataframe()
        st.dataframe(
            trials_df[[
                "number",
                "value",
                "params_rebate_percentage",
                "params_maker_taker_ratio",
                "params_position_size_pct",
                "state"
            ]].sort_values("value", ascending=False),
            use_container_width=True
        )

        st.download_button(
            "📥 Download Trial Data",
            trials_df.to_csv(index=False),
            "optimization_results.csv",
            "text/csv"
        )


# Footer with info
st.divider()
st.markdown("""
### About This Tool

This sandbox uses **Optuna** to optimize trading rebate parameters:

- **Rebate Percentage**: The commission rebate from the exchange
- **Maker/Taker Ratio**: Proportion of orders providing liquidity (makers)
- **Position Size**: Percentage of capital allocated per trade

The optimizer maximizes the **Sharpe ratio** while accounting for transaction costs and rebates.

**Note**: This is a simulation tool. Real trading results may vary based on market conditions,
execution quality, and actual rebate agreements with exchanges.
""")
