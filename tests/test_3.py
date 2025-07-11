import pytest
import pandas as pd
from definition_7e2ac3a03367456aa1ca31f297a9ea02 import generate_portfolio_data

@pytest.mark.parametrize("num_deals, risk_range, return_range, skewed, expected_columns", [
    (10, (0.01, 0.1), (0.05, 0.2), False, ['Risk_Score', 'Return_Ratio']),
    (5, (0.0, 0.05), (0.1, 0.15), True, ['Risk_Score', 'Return_Ratio']),
    (0, (0.0, 0.05), (0.1, 0.15), True, ['Risk_Score', 'Return_Ratio']),
])
def test_generate_portfolio_data_basic(num_deals, risk_range, return_range, skewed, expected_columns):
    df = generate_portfolio_data(num_deals, risk_range, return_range, skewed)
    assert isinstance(df, pd.DataFrame)
    if num_deals > 0:
        assert not df.empty
    assert list(df.columns) == expected_columns

@pytest.mark.parametrize("risk_range, return_range", [
    ((0.1, 0.01), (0.05, 0.2)),  # Invalid range
    ((0.01, 0.1), (0.2, 0.05)),  # Invalid range
])
def test_generate_portfolio_data_invalid_range(risk_range, return_range):
    with pytest.raises(ValueError):
        generate_portfolio_data(5, risk_range, return_range, False)

def test_generate_portfolio_data_skewed_distribution():
    num_deals = 100
    risk_range = (0.01, 0.1)
    return_range = (0.05, 0.2)
    skewed = True
    df = generate_portfolio_data(num_deals, risk_range, return_range, skewed)
    # Basic check for skewed behavior - more deals closer to min risk/return
    risk_threshold = risk_range[0] + (risk_range[1] - risk_range[0]) * 0.25
    return_threshold = return_range[0] + (return_range[1] - return_range[0]) * 0.25
    
    low_risk_low_return_count = len(df[(df['Risk_Score'] <= risk_threshold) & (df['Return_Ratio'] <= return_threshold)])
    assert low_risk_low_return_count > num_deals * 0.2  # Expect at least 20% in the lower quadrant

@pytest.mark.parametrize("num_deals", [
    (5),
    (10),
])
def test_generate_portfolio_data_values_within_range(num_deals):
    risk_range = (0.01, 0.1)
    return_range = (0.05, 0.2)
    df = generate_portfolio_data(num_deals, risk_range, return_range, False)
    assert df['Risk_Score'].min() >= risk_range[0]
    assert df['Risk_Score'].max() <= risk_range[1]
    assert df['Return_Ratio'].min() >= return_range[0]
    assert df['Return_Ratio'].max() <= return_range[1]
