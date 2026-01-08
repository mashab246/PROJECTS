from smarthome.energy_consumer import EnergyConsumer
        
class HVAC(EnergyConsumer):
    def __init__(self, name, rated_power_watts, current_temp, target_low, target_high):
        super().__init__(name, rated_power_watts)
        self.current_temp = float(current_temp)
        # If targets are not provided, set reasonable defaults around current_temp
        self.target_low = float(target_low) 
        self.target_high = float(target_high) 
        self.mode = 'off'
        
    def set_target_temps(self, low, high):
        """Set low/high target temps (°C) and re-evaluate operation."""
        self.target_low = float(low)
        self.target_high = float(high)
        print(f"{self.name} target temperature range set to {self.target_low}°C - {self.target_high}°C")
        self.update_temperature()

    def update_temperature(self):
        #check temp and adjust heating or cooling
        if self.current_temp < self.target_low:
            self.mode = "heating"
            self.activate()
            self.current_temp += 1
            return(f"{self.name} is heating. Current temperature: {self.current_temp}°C")
            
        elif self.current_temp > self.target_high:
            self.mode = "cooling"
            self.activate()
            self.current_temp -= 1
            return(f"{self.name} is cooling. Current temperature: {self.current_temp}°C")
            
        else:
            self.mode = "off"
            self.deactivate()
            
        print(f"{self.name} mode: {self.mode}, temperature: {self.current_temp}°C")