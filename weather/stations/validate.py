
class Validator:
    def __init__(self, fields):
        self.fields = fields

    def get_value(self, field, default):
        return self.fields.get(field, default)

    def validate(self):
        assert 0 <= self.get_value('HumOut', -1) <= 100
        assert 0 <= self.get_value('HumIn', -1) <= 100
        assert -120 <= self.get_value('DewPoint', -1) <= 254
        
        assert -20 <= self.get_value('TempIn', -255) <= 254
        assert -120 <= self.get_value('TempOut', -255) <= 254
        assert -254 <= self.get_value('WindChill', -255) <= 254
        assert -120 <= self.get_value('HeatIndex', -255) <= 254
        
        assert 0 <= self.get_value('RainYear', -1) <= 254
        assert 0 <= self.get_value('RainMonth', -1) <= 254
        assert 0 <= self.get_value('RainDay', -1) <= 254
        assert 0 <= self.get_value('RainStorm', -1) <= 254

        assert 0 <= self.get_value('WindSpeed', -1) <= 200
        assert 0 <= self.get_value('WindSpeed10Min', -1) <= 200
        assert 0 <= self.get_value('WindDir', -1) <= 359

        assert 26.00 <= self.get_value('Pressure', -1) <= 34.00
