import pytest
import pandas as pd
from definition_a4c10aab14a44ae997a1b02b219526e6 import display_scenarios_comparison

def create_mock_dataframe(data):
    return pd.DataFrame(data)

def scenarios_equal(scenarios1, scenarios2):
    if len(scenarios1) != len(scenarios2):
        return False

    for i in range(len(scenarios1)):
        if scenarios1[i].keys() != scenarios2[i].keys():
            return False
        for key in scenarios1[i]:
            if key == 'df':
                if not scenarios1[i][key].equals(scenarios2[i][key]):
                    return False
            elif scenarios1[i][key] != scenarios2[i][key]:
                return False
    return True

@pytest.fixture
def mock_pandas_dataframe(monkeypatch):
    """Mocks pd.DataFrame to check what data is passed to it."""
    mock_calls = []

    def mock_dataframe(data=None, *args, **kwargs):
        mock_calls.append({"data": data, "args": args, "kwargs": kwargs})
        return create_mock_dataframe(data)

    monkeypatch.setattr(pd, "DataFrame", mock_dataframe)
    return mock_calls

@pytest.mark.parametrize("scenarios_list, expected_data", [
    (
        [
            {
                "scenario_name": "Scenario 1",
                "parameters": {"loan_amount": 100000},
                "results": {"rarorac": 0.15},
            },
            {
                "scenario_name": "Scenario 2",
                "parameters": {"loan_amount": 200000},
                "results": {"rarorac": 0.20},
            },
        ],
        [
            {"scenario_name": "Scenario 1", "parameters": {"loan_amount": 100000}, "results": {"rarorac": 0.15}, "df": create_mock_dataframe(
                {
                    "scenario_name": ["Scenario 1", "Scenario 2"],
                    "loan_amount": [100000, 200000],
                    "rarorac": [0.15, 0.20]
                }
            )}
        ]
    ),
    (
        [],
        []
    ),
    (
        [
            {
                "scenario_name": "Scenario 3",
                "parameters": {"interest_rate": 0.05},
                "results": {"expected_loss": 1000},
            }
        ],
        [
            {
                "scenario_name": "Scenario 3", "parameters": {"interest_rate": 0.05}, "results": {"expected_loss": 1000}, "df": create_mock_dataframe(
                    {
                        "scenario_name": ["Scenario 3"],
                        "interest_rate": [0.05],
                        "expected_loss": [1000]
                    }
                )}
        ]
    ),
    (
         [
            {
                "scenario_name": "Scenario 1",
                "parameters": {"loan_amount": 100000, "interest_rate": 0.05},
                "results": {"rarorac": 0.15, "deal_outcome": "Meets Hurdle Rate"},
            },
            {
                "scenario_name": "Scenario 2",
                "parameters": {"loan_amount": 200000, "interest_rate": 0.06},
                "results": {"rarorac": 0.20, "deal_outcome": "Exceeds Hurdle Rate"},
            },
        ],
        [
            {"scenario_name": "Scenario 1", "parameters": {"loan_amount": 100000, "interest_rate": 0.05}, "results": {"rarorac": 0.15, "deal_outcome": "Meets Hurdle Rate"}, "df": create_mock_dataframe(
                {
                    "scenario_name": ["Scenario 1", "Scenario 2"],
                    "loan_amount": [100000, 200000],
                    "interest_rate": [0.05, 0.06],
                    "rarorac": [0.15, 0.20],
                    "deal_outcome": ["Meets Hurdle Rate", "Exceeds Hurdle Rate"]
                }
            )}
        ]

    ),
    (
        [
            {
                "scenario_name": "Scenario A",
                "parameters": {},
                "results": {},
            },
            {
                "scenario_name": "Scenario B",
                "parameters": {},
                "results": {},
            },
        ],
        [
            {"scenario_name": "Scenario A", "parameters": {}, "results": {}, "df": create_mock_dataframe({"scenario_name": ["Scenario A", "Scenario B"]})}
        ]
    )
])
def test_display_scenarios_comparison(scenarios_list, expected_data, mock_pandas_dataframe):
    display_scenarios_comparison(scenarios_list)

    if len(scenarios_list) > 0 :
        first_scenario = scenarios_list[0]
        parameter_keys = list(first_scenario['parameters'].keys())
        result_keys = list(first_scenario['results'].keys())
        columns = ['scenario_name'] + parameter_keys + result_keys
    else:
        columns = ['scenario_name']
    
    
    data = {}
    data['scenario_name'] = [s['scenario_name'] for s in scenarios_list]
    
    for param in columns[1:]:
        data[param] = [s['parameters'].get(param, s['results'].get(param)) for s in scenarios_list]

    expected_df = pd.DataFrame(data)
    
    if len(mock_pandas_dataframe) > 0:
        pd_call = mock_pandas_dataframe[0]
        pd_data = pd_call['data']

        assert expected_df.equals(pd_data)

    else:
        assert len(scenarios_list) == 0


