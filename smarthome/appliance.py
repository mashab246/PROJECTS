from smarthome.energy_consumer import EnergyConsumer

class Appliance(EnergyConsumer):
    def __init__(self, name, rated_power_watts):
        super().__init__(name, rated_power_watts)
        
        self.available_cycles = ["normal", "eco", "intensive"]
        self.current_cycle = None
        
    def start_cycle(self, cycle_name):
        if cycle_name not in self.available_cycles:
            return(f"Cycle '{cycle_name}' is not supported.")
        
        if self.is_active:
            self.current_cycle = cycle_name
            self.activate()
            return(f"Starting {self.current_cycle} cycle on {self.name}.")
       
            
    def stop_cycle(self):
        if not self.is_active:
            self.deactivate()
            
            return(f"{self.name} cycle stopped.")
            