from smarthome.energy_consumer import EnergyConsumer

class Appliance(EnergyConsumer):
    def __init__(self, name, power_consumption):
        super().__init__(name, power_consumption)
        self.status = None
        self.available_cycles = ["normal", "eco", "intensive"]
        self.current_cycle = None
        
    def start_cycle(self, cycle_name):
        if cycle_name in self.available_cycles:
            self.current_cycle = cycle_name
            self.activate()
            self.status = "running"
            
            print(f"Starting {self.current_cycle} cycle on {self.name}.")
        else:
            print(f"Error: Cycle {cycle_name} not available for cycle.")
            
    def stop_cycle(self):
        if self.status == "running":
            self.deactivate()
            self.status = "stopped"
            
            print(f"{self.name} cycle stopped.")
            