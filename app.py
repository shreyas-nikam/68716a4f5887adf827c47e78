
import streamlit as st
st.set_page_config(page_title=\"QuLab\", layout=\"wide\")
st.sidebar.image(\"https://www.quantuniversity.com/assets/img/logo5.jpg\")
st.sidebar.divider()
st.title(\"QuLab: Risk Management Framework Lab 2\")
st.divider()
st.markdown(r\"
In this lab, you will explore the Risk-Adjusted Return on Risk-Adjusted Capital (RARORAC) metric and interactive risk-sensitive pricing tools, applying the core elements of the **Risk Management Framework** utilized across financial institutions.

**Business logic and learning points:**
- Financial institutions assess the adequacy of returns for the risks they accept with each deal, using RARORAC (Risk-Adjusted Return on Risk-Adjusted Capital).
- You will interact with parameters like loan amount, interest rate, fees, operating costs, expected loss, and capital allocation to see their direct effect on performance metrics.
- Compare different hypothetical deal scenarios for better intuition about portfolio management.
- Visualize how risk/return distribution impacts overall portfolio quality and understand how skewed risk-taking can erode value for financial institutions.

Navigate through all pages to:
- Compute RARORAC and understand its drivers.
- Save and compare deal scenarios.
- Explore how portfolio quality is visualized and how risk-sensitive pricing can mitigate skewed risk-taking.
\")
st.markdown(\"---\")

st.subheader(\"RARORAC Formulae\")
st.latex(r"""
    \text{Income\_From\_Deal} = \text{Loan\_Amount} \times \text{Interest\_Rate} + \text{Fees}
""")
st.latex(r"""
    \text{Operating\_Costs} = \text{Income\_From\_Deal} \times \text{Operating\_Cost\_Ratio}
""")
st.latex(r"""
    \text{Expected\_Loss} = \text{Loan\_Amount} \times \text{Expected\_Loss\_Rate}
""")
st.latex(r"""
    \text{Net\_Risk\_Adjusted\_Reward} = \text{Income\_From\_Deal} - \text{Operating\_Costs} - \text{Expected\_Loss}
""")
st.latex(r"""
    \text{Risk\_Adjusted\_Capital} = \text{Loan\_Amount} \times \text{Unexpected\_Loss\_Capital\_Allocation\_Factor}
""")
st.latex(r"""
    \text{RARORAC} = \frac{\text{Net\_Risk\_Adjusted\_Reward}}{\text{Risk\_Adjusted\_Capital}}
""")

page = st.sidebar.selectbox(label=\"Navigation\", options=[\"RARORAC Calculator\", \"Scenario Comparison\", \"Portfolio Quality Visualization\"])

if page == \"RARORAC Calculator\":
    from application_pages.page1 import run_page1
    run_page1()
elif page == \"Scenario Comparison\":
    from application_pages.page2 import run_page2
    run_page2()
elif page == \"Portfolio Quality Visualization\":
    from application_pages.page3 import run_page3
    run_page3()

st.markdown(\"---\")
st.subheader(\"References\")
st.markdown(r\"
[15] *Operational Risk Manager Handbook*, Chapter 3: The Risk Management Framework, 'Risk Pricing' subsection.  
[16] *Operational Risk Manager Handbook*, Chapter 3: The Risk Management Framework, 'Components of Determining Risk Pricing' subsection.  
[17] *Operational Risk Manager Handbook*, Chapter 3: The Risk Management Framework, 'The Denominator' subsection.  
[18] *Operational Risk Manager Handbook*, Chapter 3: The Risk Management Framework, 'Risk Insensitive Pricing and Client / Counterparty Behavior' and 'Risk Sensitive Pricing' subsections, referencing Figure 4: Portfolio Quality Distribution.
\")
