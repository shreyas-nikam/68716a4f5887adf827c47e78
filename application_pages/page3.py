
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
    st.header("📈 Portfolio Quality Visualization")
    
    # Introduction and Instructions
    st.markdown("""
    ### 📋 **About Portfolio Quality Analysis**
    
    This page helps you visualize how risk and return are distributed across your portfolio of deals. Understanding portfolio quality is crucial for:
    
    **Key Concepts:**
    - **Risk Score**: Represents the expected loss rate of each deal
    - **Return Ratio**: Represents the RARORAC of each deal
    - **Portfolio Quality**: How well your deals balance risk and return
    - **Skewed Portfolios**: Concentration in high-risk, low-return areas (bad!)
    - **Balanced Portfolios**: Good distribution across risk-return spectrum (good!)
    
    **What to look for:**
    - ✅ **Good Portfolio**: Deals clustered in low-risk, high-return areas
    - ❌ **Poor Portfolio**: Too many deals in high-risk, low-return areas
    - 🎯 **Ideal**: Most deals above the hurdle rate line
    """)
    
    st.markdown("---")
    
    st.markdown("Visualize portfolio risk/return distribution based on your saved scenarios, or explore with synthetic data.")

    # Check if there are saved scenarios
    if st.session_state.saved_scenarios:
        st.subheader("🎯 Your Real Portfolio Analysis")
        st.markdown(f"""
        **Analyzing {len(st.session_state.saved_scenarios)} saved scenarios** from your RARORAC calculations.
        Each point represents one of your saved deal scenarios.
        """)
        
        # Extract data from saved scenarios
        portfolio_data = []
        for scenario_name, scenario_data in st.session_state.saved_scenarios.items():
            results = scenario_data["results"]
            parameters = scenario_data["parameters"]
            
            # Use Expected Loss Rate as Risk Score and RARORAC as Return Ratio
            risk_score = parameters.get("expected_loss_rate", 0)
            return_ratio = results.get("RARORAC", 0)
            
            portfolio_data.append({
                'Scenario_Name': scenario_name,
                'Risk_Score': risk_score,
                'Return_Ratio': return_ratio,
                'Deal_Outcome': results.get("Deal_Outcome", "Unknown")
            })
        
        df_real = pd.DataFrame(portfolio_data)
        
        # Create scatter plot with real data
        chart_real = alt.Chart(df_real).mark_point(size=100).encode(
            x=alt.X('Risk_Score', axis=alt.Axis(title='Risk Score (Expected Loss Rate)')),
            y=alt.Y('Return_Ratio', axis=alt.Axis(title='Return Ratio (RARORAC)')),
            color=alt.Color('Deal_Outcome', 
                          scale=alt.Scale(range=['red', 'green']),
                          legend=alt.Legend(title="Deal Outcome")),
            tooltip=['Scenario_Name', 'Risk_Score', 'Return_Ratio', 'Deal_Outcome']
        ).properties(
            title='Your Portfolio Quality Distribution (From Saved Scenarios)',
            width=600,
            height=400
        ).interactive()

        st.altair_chart(chart_real, use_container_width=True)
        
        # Portfolio Analysis
        st.subheader("📊 Portfolio Performance Summary")
        
        # Display summary statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📈 Total Scenarios", len(df_real))
        with col2:
            meets_hurdle = len(df_real[df_real['Deal_Outcome'] == 'Meets Hurdle Rate'])
            success_rate = (meets_hurdle / len(df_real)) * 100
            st.metric("✅ Success Rate", f"{success_rate:.1f}%")
        with col3:
            avg_rarorac = df_real['Return_Ratio'].mean()
            st.metric("📊 Avg RARORAC", f"{avg_rarorac:.2%}")
        with col4:
            avg_risk = df_real['Risk_Score'].mean()
            st.metric("⚠️ Avg Risk", f"{avg_risk:.2%}")
            
        # Portfolio Quality Assessment
        st.subheader("🎯 Portfolio Quality Assessment")
        
        if success_rate >= 80:
            st.success("🎉 **Excellent Portfolio!** Most of your deals meet the hurdle rate.")
        elif success_rate >= 60:
            st.warning("⚡ **Good Portfolio** but room for improvement. Consider reducing risk or improving returns.")
        else:
            st.error("🚨 **Portfolio Needs Attention!** Too many deals fail to meet the hurdle rate.")
            
        # Risk-Return Analysis
        high_risk_deals = len(df_real[df_real['Risk_Score'] > df_real['Risk_Score'].median()])
        if high_risk_deals > len(df_real) * 0.6:
            st.warning(f"⚠️ **High Risk Concentration**: {high_risk_deals} out of {len(df_real)} deals are above median risk.")
            
        st.markdown("---")
        
    else:
        st.info("🔍 **No saved scenarios found.** Go to 'RARORAC Calculator & Scenarios' to create and save some scenarios first!")
        st.markdown("**Why create scenarios first?** Real portfolio analysis is much more meaningful than synthetic data!")
        st.markdown("---")
    
    # Optional synthetic data section
    with st.expander("🧪 Explore with Synthetic Portfolio Data", expanded=not bool(st.session_state.saved_scenarios)):
        st.markdown("Generate synthetic portfolio data to understand portfolio quality concepts.")

    # Optional synthetic data section
    with st.expander("🧪 Explore Portfolio Concepts with Synthetic Data", expanded=not bool(st.session_state.saved_scenarios)):
        st.markdown("""
        **Learning Opportunity:** Use synthetic data to understand portfolio quality concepts before applying them to real scenarios.
        
        **Experiment with:**
        - Different portfolio sizes (number of deals)
        - Various risk ranges
        - Normal vs. skewed distributions
        - Impact on overall portfolio quality
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎛️ Portfolio Parameters")

            num_deals = st.number_input(
                label="Number of Deals",
                min_value=10,
                max_value=500,
                value=100,
                step=10
            )
            st.caption("📊 More deals = better statistical representation")

            risk_range = st.slider(
                label="Risk Score Range",
                min_value=0.01,
                max_value=0.99,
                value=(0.1, 0.5),
                step=0.01
            )
            st.caption("⚠️ Range of expected loss rates in the portfolio")

        with col2:
            st.subheader("📈 Return Parameters")
            
            return_range = st.slider(
                label="Return Ratio Range",
                min_value=0.01,
                max_value=0.50,
                value=(0.05, 0.20),
                step=0.01
            )
            st.caption("💰 Range of RARORAC values in the portfolio")

            skewed = st.checkbox("Generate Skewed Portfolio", value=False)
            st.caption("🔄 Toggle to see how skewed risk-taking affects portfolio quality")

        # Generate portfolio data
        portfolio_data = generate_portfolio_data(num_deals, risk_range, return_range, skewed)

        # Create the scatter plot
        chart = alt.Chart(portfolio_data).mark_point(opacity=0.6).encode(
            x=alt.X('Risk_Score', axis=alt.Axis(title='Risk Score (Expected Loss Rate)')),
            y=alt.Y('Return_Ratio', axis=alt.Axis(title='Return Ratio (RARORAC)')),
            tooltip=['Risk_Score', 'Return_Ratio']
        ).properties(
            title=f'{"Skewed" if skewed else "Balanced"} Synthetic Portfolio Distribution ({num_deals} deals)',
            width=600,
            height=400
        ).interactive()

        st.altair_chart(chart, use_container_width=True)
        
        # Analysis of synthetic portfolio
        st.subheader("📊 Synthetic Portfolio Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_risk = portfolio_data['Risk_Score'].mean()
            st.metric("📈 Average Risk", f"{avg_risk:.2%}")
        with col2:
            avg_return = portfolio_data['Return_Ratio'].mean()
            st.metric("💰 Average Return", f"{avg_return:.2%}")
        with col3:
            risk_return_ratio = avg_return / avg_risk if avg_risk > 0 else 0
            st.metric("🎯 Return/Risk Ratio", f"{risk_return_ratio:.2f}")
            
        if skewed:
            st.warning("⚠️ **Skewed Portfolio**: Notice how deals cluster in high-risk, low-return areas. This is bad for portfolio quality!")
        else:
            st.success("✅ **Balanced Portfolio**: Deals are well-distributed across the risk-return spectrum.")
            
        st.markdown("""
        **💡 Key Insights:**
        - **Balanced portfolios** have better risk-adjusted returns
        - **Skewed portfolios** concentrate risk in unfavorable areas
        - **Portfolio diversification** helps manage overall risk
        - **Risk-sensitive pricing** can prevent skewed risk-taking
        """)
