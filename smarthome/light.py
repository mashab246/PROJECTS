from smarthome.energy_consumer import EnergyConsumer

class Light(EnergyConsumer):
    def __init__(self, name, rated_power_watts):
        super().__init__(name, rated_power_watts)
        self.original_rated_power_watts = float(rated_power_watts)
        self.brightness_level = 0.0 #value btn 0.0 and 1.0

    def set_brightness(self, level):
        """
        Set brightness of the light.
        0.0 = OFF
        1.0 = FULL brightness
        """
        
        self.brightness_level = max(0.0, min(1.0, float(level)))
        
        if self.brightness_level == 0.0:
            self.deactivate()
           
        else:
            self.activate()

        return(f"{self.name} brightness set to {self.brightness_level * 100}%")
    
    def get_consumption(self):
        """Return actual power usage based on brightness."""
        if not self.is_active:
            return 0.0
        return self.power_consumption * self.brightness