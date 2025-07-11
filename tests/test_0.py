import pytest
from definition_2262e8546eb14dcfa4ac027906eca39e import calculate_rarorac_metrics

@pytest.mark.parametrize("loan_amount, interest_rate, fees, operating_cost_ratio, expected_loss_rate, ul_capital_factor, hurdle_rate, expected", [
    (1000000, 0.05, 10000, 0.20, 0.01, 0.10, 0.15, {'Income_From_Deal': 60000.0, 'Operating_Costs': 12000.0, 'Expected_Loss': 10000.0, 'Net_Risk_Adjusted_Reward': 38000.0, 'Risk_Adjusted_Capital': 100000.0, 'RARORAC': 0.38, 'Deal_Outcome': 'Meets Hurdle Rate'}),
    (0, 0.05, 0, 0.20, 0.01, 0.10, 0.15, {'Income_From_Deal': 0.0, 'Operating_Costs': 0.0, 'Expected_Loss': 0.0, 'Net_Risk_Adjusted_Reward': 0.0, 'Risk_Adjusted_Capital': 0.0, 'RARORAC': 0.0, 'Deal_Outcome': 'Below Hurdle Rate'}),
    (1000000, 0, 0, 0.20, 0.01, 0.10, 0.15, {'Income_From_Deal': 0.0, 'Operating_Costs': 0.0, 'Expected_Loss': 10000.0, 'Net_Risk_Adjusted_Reward': -10000.0, 'Risk_Adjusted_Capital': 100000.0, 'RARORAC': -0.1, 'Deal_Outcome': 'Below Hurdle Rate'}),
    (1000000, 0.05, 10000, 0, 0, 0.10, 0.15, {'Income_From_Deal': 60000.0, 'Operating_Costs': 0.0, 'Expected_Loss': 0.0, 'Net_Risk_Adjusted_Reward': 60000.0, 'Risk_Adjusted_Capital': 100000.0, 'RARORAC': 0.6, 'Deal_Outcome': 'Meets Hurdle Rate'}),
    (1000000, 0.05, 10000, 0.20, 0.01, 0, 0.15, {'Income_From_Deal': 60000.0, 'Operating_Costs': 12000.0, 'Expected_Loss': 10000.0, 'Net_Risk_Adjusted_Reward': 38000.0, 'Risk_Adjusted_Capital': 0.0, 'RARORAC': float('inf'), 'Deal_Outcome': 'Meets Hurdle Rate'})
])
def test_calculate_rarorac_metrics(loan_amount, interest_rate, fees, operating_cost_ratio, expected_loss_rate, ul_capital_factor, hurdle_rate, expected):
    if ul_capital_factor == 0:
        with pytest.raises(ZeroDivisionError):
            calculate_rarorac_metrics(loan_amount, interest_rate, fees, operating_cost_ratio, expected_loss_rate, ul_capital_factor, hurdle_rate)
    else:
        result = calculate_rarorac_metrics(loan_amount, interest_rate, fees, operating_cost_ratio, expected_loss_rate, ul_capital_factor, hurdle_rate)
        for key, value in expected.items():
            if key == 'RARORAC' and value != float('inf'):
                assert abs(result[key] - value) < 0.001
            elif key == 'RARORAC' and value == float('inf'):
                assert result[key] == value
            else:
                assert result[key] == value
