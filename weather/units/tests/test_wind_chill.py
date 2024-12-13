def test_calculate_wind_chill():
    assert calculate_wind_chill(0, 10) == -4.6
    assert calculate_wind_chill(10, 20) == 3.6
    assert calculate_wind_chill(15, 10) == 15  # Temperature above 10°C, should return the temperature itself
    assert calculate_wind_chill(0, 4) == 0  # Wind speed below 4.8 km/h, should return the temperature itself

test_calculate_wind_chill()
