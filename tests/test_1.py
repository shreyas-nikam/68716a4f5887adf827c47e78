import pytest
from definition_9ad6ad45e77540779e5f9eb4c6fe6da9 import save_scenario

@pytest.fixture
def scenario_data():
    return {
        "scenario_name": "Test Scenario",
        "current_parameters": {"param1": 100, "param2": 0.05},
        "current_results": {"rarorac": 0.12, "deal_outcome": "Meets Hurdle Rate"}
    }


def test_save_scenario_valid_data(scenario_data):
    try:
        save_scenario(scenario_data["scenario_name"], scenario_data["current_parameters"], scenario_data["current_results"])
        assert True  # If no error, the test passes.  We have to assert something.
    except Exception:
        assert False  # The test should not raise an exception.
        
def test_save_scenario_empty_name():
    try:
        save_scenario("", {"param1": 100}, {"rarorac": 0.12})
        assert True #If no error, the test passes.
    except Exception:
        assert False #The test should not raise an exception

def test_save_scenario_none_parameters():
    try:
        save_scenario("Scenario with no parameters", None, {"rarorac": 0.10})
        assert True
    except Exception:
        assert False

def test_save_scenario_invalid_parameter_type():
    with pytest.raises(TypeError):
        save_scenario("Invalid Parameters", 123, {"rarorac": 0.10})
        
def test_save_scenario_no_results():
     try:
        save_scenario("No Results", {"param1": 100}, None)
        assert True
     except Exception:
        assert False
