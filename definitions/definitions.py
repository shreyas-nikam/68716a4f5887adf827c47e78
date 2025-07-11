def calculate_rarorac_metrics(loan_amount, interest_rate, fees, operating_cost_ratio, expected_loss_rate, ul_capital_factor, hurdle_rate):
    """Computes RARORAC metrics."""

    Income_From_Deal = loan_amount * interest_rate + fees
    Operating_Costs = Income_From_Deal * operating_cost_ratio
    Expected_Loss = loan_amount * expected_loss_rate
    Net_Risk_Adjusted_Reward = Income_From_Deal - Operating_Costs - Expected_Loss
    Risk_Adjusted_Capital = loan_amount * ul_capital_factor

    if Risk_Adjusted_Capital == 0:
        RARORAC = float('inf')
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

SAVED_SCENARIOS = {}
            
def save_scenario(scenario_name, current_parameters, current_results):
                """Stores the current set of input parameters and their calculated RARORAC results."""
                
                global SAVED_SCENARIOS
                
                if not isinstance(scenario_name, str):
                    raise TypeError("Scenario name must be a string.")
                
                if current_parameters is not None and not isinstance(current_parameters, dict):
                    raise TypeError("Current parameters must be a dictionary or None.")
                    
                if current_results is not None and not isinstance(current_results, dict):
                    raise TypeError("Current results must be a dictionary or None.")
                
                SAVED_SCENARIOS[scenario_name] = {
                    "parameters": current_parameters,
                    "results": current_results
                }

import pandas as pd

def display_scenarios_comparison(scenarios_list):
    """Presents a tabular comparison of all saved scenarios.
    Args:
        scenarios_list: List of dictionaries, each containing scenario name, parameters, and results.
    Output:
        A pandas DataFrame displayed as a table.
    """
    if not scenarios_list:
        return

    data = {}
    # Extract scenario names
    data['scenario_name'] = [scenario['scenario_name'] for scenario in scenarios_list]

    # Extract all unique parameters and results keys
    all_keys = set()
    for scenario in scenarios_list:
        all_keys.update(scenario['parameters'].keys())
        all_keys.update(scenario['results'].keys())

    # Add parameters and results to the data dictionary
    for key in all_keys:
        values = []
        for scenario in scenarios_list:
            # Prioritize parameters over results if a key exists in both
            if key in scenario['parameters']:
                values.append(scenario['parameters'][key])
            elif key in scenario['results']:
                values.append(scenario['results'][key])
            else:
                values.append(None)  # Handle missing values

        data[key] = values

    df = pd.DataFrame(data)
    return df

import pandas as pd
import numpy as np

def generate_portfolio_data(num_deals, risk_range, return_range, skewed):
    """Generates synthetic portfolio data."""

    if risk_range[0] > risk_range[1] or return_range[0] > return_range[1]:
        raise ValueError("Invalid range: min > max")

    if num_deals <= 0:
        return pd.DataFrame({'Risk_Score': [], 'Return_Ratio': []})

    if skewed:
        risk_scores = np.random.beta(2, 8, num_deals) * (risk_range[1] - risk_range[0]) + risk_range[0]
        return_ratios = np.random.beta(2, 8, num_deals) * (return_range[1] - return_range[0]) + return_range[0]
    else:
        risk_scores = np.random.uniform(risk_range[0], risk_range[1], num_deals)
        return_ratios = np.random.uniform(return_range[0], return_range[1], num_deals)

    df = pd.DataFrame({'Risk_Score': risk_scores, 'Return_Ratio': return_ratios})
    return df