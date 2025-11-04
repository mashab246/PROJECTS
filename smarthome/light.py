from smarthome.energy_consumer import EnergyConsumer

class Light(EnergyConsumer):
    def __init__(self, name, power_consumption):
        # store the original rated power so scaling is computed from the base value
        super().__init__(name, power_consumption)
        self.original_power_consumption = float(power_consumption)
        self.brightness_level = 0.0
        # ensure power_consumption reflects initial brightness (off)
        self.power_consumption = 0.0

    def set_brightness(self, level):
        # clamp and normalize level to [0.0, 1.0]
        self.brightness_level = max(0.0, min(1.0, float(level)))
        if self.brightness_level > 0.0:
            self.activate()
            # compute scaled consumption from the original rated power
            self.power_consumption = self.original_power_consumption * self.brightness_level
        else:
            self.deactivate()
            self.power_consumption = 0.0

        print(f"{self.name} brightness set to {self.brightness_level * 100}%")