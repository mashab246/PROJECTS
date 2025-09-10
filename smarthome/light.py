from smarthome.energy_consumer import EnergyConsumer

class Light(EnergyConsumer):
    def __init__(self, name, power_consumption):
        super().__init__(name, power_consumption)
        self.original_power_consumption = power_consumption
        self.brightness_level = 0
        
    def set_brightness(self, level):
        self.brightness_level = max(0, min(1.0, level))
        if self.brightness_level > 0:
            self.activate()
            self.power_consumption = self.original_power_consumption * self.brightness_level
        else:
            self.deactivate()
            self.power_consumption = 0
            
        print(f"{self.name} brightness set to {self.brightness_level * 100}%")