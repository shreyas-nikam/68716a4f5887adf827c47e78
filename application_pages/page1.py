import streamlit as st
import pandas as pd
import numpy as np

def save_scenario_streamlit(scenario_name, current_parameters, current_results):
    """Stores the current set of input parameters and their calculated RARORAC results in session state."""
    if not isinstance(scenario_name, str):
        raise TypeError("Scenario name must be a string.")
    if current_parameters is not None and not isinstance(current_parameters, dict):
        raise TypeError("Current parameters must be a dictionary or None.")
    if current_results is not None and not isinstance(current_results, dict):
        raise TypeError("Current results must be a dictionary or None.")
    
    st.session_state.saved_scenarios[scenario_name] = {
        "parameters": current_parameters,
        "results": current_results
    }

def display_scenarios_comparison_streamlit(scenarios_dict):
    """Presents a tabular comparison of all saved scenarios from session state."""
    if not scenarios_dict:
        st.info("No scenarios saved yet. Calculate a RARORAC and click 'Save Scenario' to add it here.")
        return pd.DataFrame()

    scenarios_list_for_df = []
    for scenario_name, scenario_data in scenarios_dict.items():
        combined_data = {"Scenario Name": scenario_name}
        # Include a subset of parameters for clarity in display if too many
        combined_data.update({k.replace('_', ' ').title(): v for k, v in scenario_data["parameters"].items()})
        combined_data.update({k.replace('_', ' ').title(): v for k, v in scenario_data["results"].items()})
        scenarios_list_for_df.append(combined_data)

    df = pd.DataFrame(scenarios_list_for_df)
    # Reorder columns to put RARORAC and Deal Outcome at the end for consistency
    cols = list(df.columns)
    if 'Deal Outcome' in cols:
        cols.remove('Deal Outcome')
        cols.append('Deal Outcome')
    if 'RARORAC' in cols:
        cols.remove('RARORAC')
        cols.append('RARORAC')
    df = df[cols]
    
    st.dataframe(df)
    return df

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
    st.header("RARORAC Calculator & Scenario Management")
    
    # Introduction and Instructions
    st.markdown("""
    ### Lab Instructions
    
    Welcome to the RARORAC (Risk-Adjusted Return on Risk-Adjusted Capital) Calculator! This lab will help you understand how financial institutions evaluate the profitability of deals while accounting for risk.
    
    **What you'll learn:**
    - How to calculate RARORAC using key financial parameters
    - The impact of different risk factors on deal profitability
    - How to compare multiple deal scenarios
    - Portfolio risk management concepts
    
    **How to use this lab:**
    1. Adjust parameters in the sidebar to see real-time RARORAC calculations
    2. Save scenarios to compare different deal configurations
    3. Analyze results to understand risk-return relationships
    4. Experiment with different values to see their impact
    """)
    
    st.markdown("---")
    
    # Formulae Section
    st.subheader(" RARORAC Calculation Formulae")
    st.markdown("""
    These are the key formulae used in RARORAC calculations. Understanding these will help you interpret the results:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Income & Cost Calculations:**")
        st.latex(r"""
            \text{Income\_From\_Deal} = \text{Loan\_Amount} \times \text{Interest\_Rate} + \text{Fees}
        """)
        st.latex(r"""
            \text{Operating\_Costs} = \text{Income\_From\_Deal} \times \text{Operating\_Cost\_Ratio}
        """)
        st.latex(r"""
            \text{Expected\_Loss} = \text{Loan\_Amount} \times \text{Expected\_Loss\_Rate}
        """)
    
    with col2:
        st.markdown("**Risk-Adjusted Metrics:**")
        st.latex(r"""
            \text{Net Risk Adjusted Reward} = \text{Income} - \text{Costs} - \text{Expected Loss}
        """)
        st.latex(r"""
            \text{Risk Adjusted Capital} = \text{Loan Amount} \times \text{UL Capital Factor}
        """)
        st.latex(r"""
            \text{RARORAC} = \frac{\text{Net Risk Adjusted Reward}}{\text{Risk Adjusted Capital}}
        """)
    
    st.markdown("---")
    
    st.markdown("Adjust the parameters in the sidebar to calculate the Risk-Adjusted Return on Risk-Adjusted Capital (RARORAC) for a hypothetical deal, then save and compare different scenarios.")

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

    st.subheader("Calculated Results")
    st.markdown("Here are the calculated metrics based on your input parameters:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Income From Deal",
            value=f"${metrics['Income_From_Deal']:.2f}"
        )
        st.info("💡 **Total revenue** generated from interest payments and fees.")

    with col2:
        st.metric(
            label="Operating Costs",
            value=f"${metrics['Operating_Costs']:.2f}"
        )
        st.info("💡 **Operational expenses** as a percentage of income.")

    with col3:
        st.metric(
            label="Expected Loss",
            value=f"${metrics['Expected_Loss']:.2f}"
        )
        st.info("**Anticipated losses** due to defaults or credit events.")

    st.markdown("---")

    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            label="Net Risk-Adjusted Reward",
            value=f"${metrics['Net_Risk_Adjusted_Reward']:.2f}"
        )
        st.info("**Final profit** after deducting all costs and expected losses.")

    with col5:
        st.metric(
            label="Risk-Adjusted Capital",
            value=f"${metrics['Risk_Adjusted_Capital']:.2f}"
        )
        st.info("**Capital allocated** to cover unexpected losses (economic capital at risk).")

    st.markdown("---")

    # RARORAC Results with enhanced presentation
    col6, col7 = st.columns(2)

    with col6:
        rarorac_value = metrics['RARORAC'] * 100 if metrics['RARORAC'] != float('inf') else float('inf')
        st.metric(
            label="RARORAC",
            value=f"{rarorac_value:.2f}%" if rarorac_value != float('inf') else "∞%",
            delta="Key Performance Indicator"
        )
        st.info("**Risk-adjusted profitability ratio** - higher is better!")

    with col7:
        deal_outcome_color = "green" if metrics['Deal_Outcome'] == 'Meets Hurdle Rate' else "red"
        outcome_emoji = "✅" if metrics['Deal_Outcome'] == 'Meets Hurdle Rate' else "❌"
        st.markdown(f"<h3 style='color:{deal_outcome_color}; text-align: center;'>{outcome_emoji} {metrics['Deal_Outcome']}</h3>", unsafe_allow_html=True)
        st.info(f"💡 RARORAC ({rarorac_value:.2f}%) vs Hurdle Rate ({hurdle_rate*100:.2f}%). The deal {'**PASSES**' if metrics['Deal_Outcome'] == 'Meets Hurdle Rate' else '**FAILS**'} the profitability test.")

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

    # Scenario Saving Section
    st.markdown("---")
    st.subheader("Save & Compare Scenarios")
    st.markdown("""
    **Why save scenarios?** Compare different deal configurations to understand:
    - Which parameters have the biggest impact on profitability
    - How risk and return trade off against each other
    - Portfolio-level effects when you have multiple deals
    """)
    
    col_save, col_clear = st.columns(2)
    
    with col_save:
        scenario_name = st.text_input("Scenario Name", placeholder="e.g., 'High Risk Deal', 'Conservative Option'")
        if st.button("Save Current Scenario", type="primary") and scenario_name:
            save_scenario_streamlit(scenario_name, st.session_state['current_rarorac_params'], st.session_state['current_rarorac_results'])
            st.success(f"Scenario '{scenario_name}' saved successfully!")
    
    with col_clear:
        st.write("")  # Empty space for alignment
        st.write("")  # Empty space for alignment
        if st.button("Clear All Scenarios", type="secondary"):
            st.session_state.saved_scenarios = {}
            st.info("All scenarios cleared.")

    # Scenario Comparison Display
    if st.session_state.saved_scenarios:
        st.subheader("Saved Scenarios Comparison")
        st.markdown(f"**{len(st.session_state.saved_scenarios)} scenario(s) saved.** Use this table to compare different deal configurations:")
        display_scenarios_comparison_streamlit(st.session_state.saved_scenarios)
        
        # Analysis tips
        st.markdown("""
        **Analysis Tips:**
        - Look for scenarios with high RARORAC that meet the hurdle rate
        - Compare how different risk factors affect profitability
        - Consider the trade-off between risk and return
        - Use these insights for portfolio-level decision making
        """)
    else:
        st.info("**Tip:** Save different scenarios to build a comparison table and analyze trade-offs between risk and return!")

