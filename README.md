# QuLab: Risk Management Framework Lab 2 - Streamlit Application

![QuLab Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## Project Description

This Streamlit application, **QuLab: Risk Management Framework Lab 2**, is designed as an interactive learning tool to explore core concepts within the Risk Management Framework used by financial institutions. Specifically, it focuses on the **Risk-Adjusted Return on Risk-Adjusted Capital (RARORAC)** metric and the principles of risk-sensitive pricing.

Users can interact with key financial parameters to calculate RARORAC for hypothetical deals, compare different scenarios, and visualize portfolio quality distributions, gaining intuition about how risk impacts profitability and value creation in a financial context.

**Learning Objectives:**

*   Understand the components and calculation of the RARORAC metric.
*   Analyze how changes in loan amount, interest rate, fees, costs, and risk factors (expected/unexpected loss) affect RARORAC.
*   Compare the risk-adjusted profitability of different deal scenarios.
*   Visualize how the distribution of risk and return across a portfolio impacts its overall quality.
*   Appreciate the importance of risk-sensitive pricing in mitigating skewed risk-taking behavior.

## Features

*   **RARORAC Calculator:** An interactive tool to input deal-specific parameters and compute the key metrics including Income, Operating Costs, Expected Loss, Net Risk-Adjusted Reward, Risk-Adjusted Capital, and the final RARORAC.
*   **Hurdle Rate Comparison:** Automatically compares the calculated RARORAC against a user-defined hurdle rate to determine the deal's outcome (Meets/Below Hurdle Rate).
*   **Scenario Saving and Comparison:** Save calculated deal scenarios with custom names and view them side-by-side in a table for easy comparison of parameters and results.
*   **Portfolio Quality Visualization:** Generate and visualize synthetic portfolio data based on user-defined ranges for risk and return. Toggle a "Skewed Portfolio" option to see how concentrating deals in high-risk/low-return areas impacts the distribution, simulating the effect of risk-insensitive pricing.
*   **Clear Navigation:** Easy switching between different tools using a sidebar navigation menu.
*   **Formula Display:** LaTeX rendering of the key RARORAC calculation formulae on the main page.
*   **Informative Tooltips:** Sidebar inputs include informative tooltips explaining each parameter.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python 3.7+ installed on your system.

The required Python libraries are:
*   streamlit
*   pandas
*   numpy
*   altair

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd <repository_directory> # Replace with the cloned directory name
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    pip install streamlit pandas numpy altair
    ```
    *(Optional but recommended)*: Create a `requirements.txt` file from the installed dependencies:
    ```bash
    pip freeze > requirements.txt
    ```
    Then, others can install dependencies using:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Streamlit application:**
    Navigate to the root directory of the project in your terminal (where `app.py` is located) and run:
    ```bash
    streamlit run app.py
    ```

2.  **Access the Application:**
    Your web browser should automatically open a new tab with the application running (usually at `http://localhost:8501`). If it doesn't, open your browser and go to that URL.

3.  **Navigate:**
    Use the `Navigation` select box in the sidebar to switch between the "RARORAC Calculator", "Scenario Comparison", and "Portfolio Quality Visualization" pages.

4.  **Interact:**
    *   **RARORAC Calculator:** Adjust the parameters in the sidebar input fields and observe the calculated metrics and deal outcome on the main page.
    *   **Scenario Comparison:** After calculating a scenario on the first page, navigate here, enter a name, and click "Save Current Scenario". Saved scenarios will appear in the table below. You can also clear all saved scenarios.
    *   **Portfolio Quality Visualization:** Adjust the number of deals, risk range, and return range in the sidebar. Toggle the "Skewed Portfolio" checkbox to see the effect on the visualization.

## Project Structure

```
.
├── app.py
└── application_pages/
    ├── __init__.py   # Makes application_pages a Python package
    ├── page1.py      # RARORAC Calculator logic and UI
    ├── page2.py      # Scenario Comparison logic and UI
    └── page3.py      # Portfolio Visualization logic and UI
```

*   `app.py`: The main entry point for the Streamlit application. Handles setup, main page content, sidebar navigation, and routing to different pages.
*   `application_pages/`: A directory containing the code for each specific page/tool within the application.
*   `page1.py`: Implements the RARORAC calculation and display logic.
*   `page2.py`: Implements the logic for saving and comparing scenarios using Streamlit's session state.
*   `page3.py`: Implements the logic for generating and visualizing synthetic portfolio data using Altair.

## Technology Stack

*   **Streamlit:** The core framework used for building the interactive web application with Python.
*   **Python:** The programming language used for the entire application logic.
*   **Pandas:** Used for data handling, particularly in the scenario comparison page (`page2.py`) and data generation (`page3.py`).
*   **NumPy:** Used for numerical operations, especially in the portfolio data generation (`page3.py`).
*   **Altair:** Used for creating interactive statistical visualizations, specifically the scatter plot in the portfolio visualization page (`page3.py`).
*   **LaTeX:** Used via Streamlit's `st.latex` for rendering mathematical formulas.

## Contributing

This project is primarily a lab exercise. While direct code contributions might not be the primary focus, suggestions for improvements, bug reports, or enhancements are welcome. Please open an issue in the repository to provide feedback.

## License

This project is created as a laboratory exercise and does not currently have a specific open-source license defined.

## Contact

This lab project is developed by Quant University. For inquiries related to Quant University programs, please visit [https://www.quantuniversity.com/](https://www.quantuniversity.com/).

