
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def generate_portfolio_data(num_deals, risk_range, return_range, skewed):
    """Generates synthetic portfolio data."""
    if risk_range[0] > risk_range[1] or return_range[0] > return_range[1]:
        raise ValueError("Invalid range: min > max")

    if num_deals <= 0:
        return pd.DataFrame({'Risk_Score': [], 'Return_Ratio': []})

    if skewed:
        # Skewed towards higher risk / lower return (more deals near boundary)
        risk_scores = np.random.beta(2, 8, num_deals) * (risk_range[1] - risk_range[0]) + risk_range[0]
        return_ratios = np.random.beta(8, 2, num_deals) * (return_range[1] - return_range[0]) + return_range[0]
    else:
        # Uniformly distributed
        risk_scores = np.random.uniform(risk_range[0], risk_range[1], num_deals)
        return_ratios = np.random.uniform(return_range[0], return_range[1], num_deals)

    df = pd.DataFrame({'Risk_Score': risk_scores, 'Return_Ratio': return_ratios})
    return df

def run_page3():
    st.header(\"Portfolio Quality Visualization\")
    st.markdown(\"Visualize portfolio risk/return distribution. Skewed portfolios concentrate deals in areas of high risk and/or low return.\")

    st.sidebar.subheader(\"Portfolio Parameters\")

    num_deals = st.sidebar.number_input(
        label=\"Number of Deals\",
        min_value=10,
        max_value=500,
        value=100,
        step=10
    )
    st.sidebar.info(\"The number of synthetic deals to generate for the portfolio.\")

    risk_range = st.sidebar.slider(
        label=\"Risk Score Range\",
        min_value=0.01,
        max_value=0.99,
        value=(0.1, 0.5),
        step=0.01
    )
    st.sidebar.info(\"The range of risk scores for the generated deals.\")

    return_range = st.sidebar.slider(
        label=\"Return Ratio Range\",
        min_value=0.01,
        max_value=0.50,
        value=(0.05, 0.20),
        step=0.01
    )
    st.sidebar.info(\"The range of return ratios for the generated deals.\")

    skewed = st.sidebar.checkbox(\"Skewed Portfolio\", value=False)
    st.sidebar.info(\"Toggle to generate a portfolio skewed towards higher risk and lower return.\")

    # Generate portfolio data
    portfolio_data = generate_portfolio_data(num_deals, risk_range, return_range, skewed)

    # Create the scatter plot
    chart = alt.Chart(portfolio_data).mark_point().encode(
        x=alt.X('Risk_Score', axis=alt.Axis(title='Risk Score')),
        y=alt.Y('Return_Ratio', axis=alt.Axis(title='Return Ratio')),
        tooltip=['Risk_Score', 'Return_Ratio']
    ).properties(
        title='Portfolio Quality Distribution'
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    # Add a conceptual "Minimum Acceptable Risk Boundary" or "Hurdle Rate" line if relevant
    # This is optional, adapt as needed, for now, it's commented out.
    # source = pd.DataFrame({
    #     'Risk_Score': [min(risk_range), max(risk_range)],
    #     'Hurdle_Return': [0.10, 0.10] # Assuming a fixed hurdle rate for demonstration
    # })
    # line = alt.Chart(source).mark_line(color='red', strokeDash=[5,5]).encode(
    #     x='Risk_Score',
    #     y='Hurdle_Return'
    # )
    # final_chart = (chart + line).interactive()
    # st.altair_chart(final_chart, use_container_width=True)
