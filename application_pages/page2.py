
import streamlit as st
import pandas as pd

# Initialize session state for saved scenarios if not already present
if 'saved_scenarios' not in st.session_state:
    st.session_state.saved_scenarios = {}

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

def run_page2():
    st.header(\"Scenario Comparison\")
    st.markdown(\"Calculate RARORAC on the first page, then save scenarios here to compare them.\")

    # Scenario Saving
    st.subheader(\"Save Current Scenario\")
    scenario_name = st.text_input(\"Scenario Name\")
    if st.button(\"Save Current Scenario\") and scenario_name:
        if 'current_rarorac_params' in st.session_state and 'current_rarorac_results' in st.session_state:
            save_scenario_streamlit(scenario_name, st.session_state['current_rarorac_params'], st.session_state['current_rarorac_results'])
            st.success(f\"Scenario '{scenario_name}' saved successfully!\")
        else:
            st.warning(\"Please calculate a RARORAC on the 'RARORAC Calculator' page first.\")

    # Scenario Comparison Display
    st.subheader(\"Compare Scenarios\")
    if st.button(\"Clear All Scenarios\"):
        st.session_state.saved_scenarios = {}
        st.info(\"All scenarios cleared.\")

    display_scenarios_comparison_streamlit(st.session_state.saved_scenarios)

