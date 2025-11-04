from smarthome.energy_consumer import EnergyConsumer
        
class HVAC(EnergyConsumer):
    def __init__(self, name, power_consumption, current_temp, target_low=None, target_high=None):
        super().__init__(name, power_consumption)
        self.current_temp = float(current_temp)
        # If targets are not provided, set reasonable defaults around current_temp
        self.target_low = float(target_low) if target_low is not None else self.current_temp - 1.0
        self.target_high = float(target_high) if target_high is not None else self.current_temp + 1.0
        self.mode = 'off'
        
    def set_target_temps(self, low, high):
        """Set low/high target temps (°C) and re-evaluate operation."""
        self.target_low = float(low)
        self.target_high = float(high)
        print(f"{self.name} target temperature range set to {self.target_low}°C - {self.target_high}°C")
        self.check_and_run()

    def check_and_run(self):
        """
        Decide mode based on current temperature and targets.
        If heating or cooling is required, activate and simulate a single step change (±1°C).
        Otherwise deactivate.
        """
        if self.current_temp < self.target_low:
            self.mode = "heating"
        elif self.current_temp > self.target_high:
            self.mode = "cooling"
        else:
            self.mode = "off"

        if self.mode in ("heating", "cooling"):
            self.activate()
            if self.mode == "heating":
                # Simulate heating step
                self.current_temp += 1
                print(f"{self.name} is heating. Current temperature: {self.current_temp}°C")
            else:
                # Simulate cooling step
                self.current_temp -= 1
                print(f"{self.name} is cooling. Current temperature: {self.current_temp}°C")
        else:
            self.deactivate()