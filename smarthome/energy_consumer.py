class EnergyConsumer:
    def __init__(self, name, rated_power_watts):
        self.name = name
        self.rated_power_watts = rated_power_watts
        self.is_active = False
        
    def activate(self):
        self.is_active = True
        return(f"{self.name} activated, consuming {self.rated_power_watts}W")
            
    def deactivate(self):
        self.is_active = False
        return(f"{self.name} deactivated, consuming 0W")
            
    def get_consumption(self):
        if self.is_active:
            return self.rated_power_watts
            
        return 0.0
           


