
import streamlit as st
import pandas as pd
import numpy as np

def calculate_rarorac_metrics(loan_amount, interest_rate, fees, operating_cost_ratio, expected_loss_rate, ul_capital_factor, hurdle_rate):
    """Computes RARORAC metrics."""
    Income_From_Deal = loan_amount * interest_rate + fees
    Operating_Costs = Income_From_Deal * operating_cost_ratio
    Expected_Loss = loan_amount * expected_loss_rate
    Net_Risk_Adjusted_Reward = Income_From_Deal - Operating_Costs - Expected_Loss
    Risk_Adjusted_Capital = loan_amount * ul_capital_factor

    if Risk_Adjusted_Capital == 0:
        RARORAC = float('inf') # Handle division by zero for RARORAC
    else:
        RARORAC = Net_Risk_Adjusted_Reward / Risk_Adjusted_Capital

    if RARORAC >= hurdle_rate:
        Deal_Outcome = 'Meets Hurdle Rate'
    else:
        Deal_Outcome = 'Below Hurdle Rate'

    return {
        'Income_From_Deal': Income_From_Deal,
        'Operating_Costs': Operating_Costs,
        'Expected_Loss': Expected_Loss,
        'Net_Risk_Adjusted_Reward': Net_Risk_Adjusted_Reward,
        'Risk_Adjusted_Capital': Risk_Adjusted_Capital,
        'RARORAC': RARORAC,
        'Deal_Outcome': Deal_Outcome
    }

def run_page1():
    st.header("RARORAC Calculator")
    st.markdown("Adjust the parameters in the sidebar to calculate the Risk-Adjusted Return on Risk-Adjusted Capital (RARORAC) for a hypothetical deal.")

    # Input parameters in Sidebar
    st.sidebar.subheader("Deal Parameters")
    loan_amount = st.sidebar.number_input(
        label="Loan Amount ($)",
        min_value=1000,
        max_value=1000000000,
        value=1000000,
        step=100000
    )
    st.sidebar.info("The total principal amount of the loan.")

    interest_rate = st.sidebar.number_input(
        label="Interest Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    ) / 100.0 # Convert to decimal
    st.sidebar.info("The annual interest rate charged on the loan.")

    fees = st.sidebar.number_input(
        label="Fees ($)",
        min_value=0,
        max_value=1000000,
        value=5000,
        step=1000
    )
    st.sidebar.info("Any additional upfront fees associated with the deal.")

    operating_cost_ratio = st.sidebar.number_input(
        label="Operating Cost Ratio (% of Income)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.1,
        format="%.2f"
    ) / 100.0 # Convert to decimal
    st.sidebar.info("The proportion of income consumed by operating costs related to the deal.")

    expected_loss_rate = st.sidebar.number_input(
        label="Expected Loss Rate (% of Loan Amount)",
        min_value=0.0,
        max_value=100.0,
        value=2.0,
        step=0.1,
        format="%.2f"
    ) / 100.0 # Convert to decimal
    st.sidebar.info("The anticipated percentage of the loan amount that may be lost due to default or other credit events.")

    ul_capital_factor = st.sidebar.number_input(
        label="Unexpected Loss Capital Allocation Factor (% of Loan Amount)",
        min_value=0.0,
        max_value=100.0,
        value=15.0,
        step=0.1,
        format="%.2f"
    ) / 100.0 # Convert to decimal
    st.sidebar.info("The percentage of the loan amount set aside as capital to cover unexpected losses, representing economic capital.")

    hurdle_rate = st.sidebar.number_input(
        label="Hurdle Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.1,
        format="%.2f"
    ) / 100.0 # Convert to decimal
    st.sidebar.info("The minimum acceptable RARORAC percentage required for a deal to be considered profitable and risk-adequate.")

    # Calculate metrics
    metrics = calculate_rarorac_metrics(
        loan_amount, interest_rate, fees, operating_cost_ratio,
        expected_loss_rate, ul_capital_factor, hurdle_rate
    )

    st.subheader("Calculated Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Income From Deal",
            value=f"${metrics['Income_From_Deal']:.2f}"
        )
        st.info("Total revenue generated from the deal, including interest and fees.")

    with col2:
        st.metric(
            label="Operating Costs",
            value=f"${metrics['Operating_Costs']:.2f}"
        )
        st.info("Costs incurred in originating and managing the deal.")

    with col3:
        st.metric(
            label="Expected Loss",
            value=f"${metrics['Expected_Loss']:.2f}"
        )
        st.info("The statistically predicted loss from the deal based on historical data and risk models.")

    st.markdown("---")

    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            label="Net Risk-Adjusted Reward",
            value=f"${metrics['Net_Risk_Adjusted_Reward']:.2f}"
        )
        st.info("The income from the deal after deducting operating costs and expected losses.")

    with col5:
        st.metric(
            label="Risk-Adjusted Capital",
            value=f"${metrics['Risk_Adjusted_Capital']:.2f}"
        )
        st.info("The capital allocated to cover unexpected losses, representing the economic capital at risk.")

    st.markdown("---")

    col6, col7 = st.columns(2)

    with col6:
        rarorac_value = metrics['RARORAC'] * 100 if metrics['RARORAC'] != float('inf') else float('inf')
        st.metric(
            label="RARORAC",
            value=f"{rarorac_value:.2f}%" if rarorac_value != float('inf') else "Infinity"
        )
        st.info("The ratio of Net Risk-Adjusted Reward to Risk-Adjusted Capital, indicating the risk-adjusted profitability.")

    with col7:
        deal_outcome_color = "green" if metrics['Deal_Outcome'] == 'Meets Hurdle Rate' else "red"
        st.markdown(f"<p style='color:{deal_outcome_color}; font-size: 24px; font-weight: bold;'>Deal Outcome: {metrics['Deal_Outcome']}</p>", unsafe_allow_html=True)
        st.info(f"Compares the calculated RARORAC ({rarorac_value:.2f}%) against the Hurdle Rate ({hurdle_rate*100:.2f}%). Determines if the deal is adequately profitable given its risk.")

    # Store current parameters and results in session state for scenario saving
    st.session_state['current_rarorac_params'] = {
        'loan_amount': loan_amount,
        'interest_rate': interest_rate,
        'fees': fees,
        'operating_cost_ratio': operating_cost_ratio,
        'expected_loss_rate': expected_loss_rate,
        'ul_capital_factor': ul_capital_factor,
        'hurdle_rate': hurdle_rate
    }
    st.session_state['current_rarorac_results'] = metrics

