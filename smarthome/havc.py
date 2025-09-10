from smarthome.energy_consumer import EnergyConsumer
        
class HVAC(EnergyConsumer):
    def  __init__(self, name, power_consumption, current_temp):
        super().__init__(name, power_consumption)
        self.current_temp = current_temp
        self.target_temp = current_temp
        self.mode = 'off'
        
    def set_target_temp(self, temp):
        self.target_temp = temp
        print(f"{self.name} target temperature set to {self.target_temp}°C")
        self.check_and_run()
        
    def check_and_run(self):
        if self.current_temp < self.target_temp:
            self.mode = "heating"
        elif self.current_temp > self.target_temp:
            self.mode = "cooling"
        else:
            self.mode = "off"
    
        if self.is_active and self.mode != "off":
            if self.mode == "heating" and self.current_temp < self.target_temp:
                self.current_temp += 1  # Simulate heating
                print(f"{self.name} is heating. Current temperature: {self.current_temp}°C")
            elif self.mode == "cooling" and self.current_temp > self.target_temp:
                self.current_temp -= 1  # Simulate cooling
                print(f"{self.name} is cooling. Current temperature: {self.current_temp}°C")
            else:
                self.deactivate()