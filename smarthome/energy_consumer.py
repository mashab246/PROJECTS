class EnergyConsumer:
    def __init__(self, name, power_consumption):
        self.name = name
        self.power_consumption = power_consumption
        self.is_active = False
        
    def activate(self):
        if not self.is_active:
            self.is_active = True
            print(f"{self.name} activated, consuming {self.power_consumption}W")
            
    def deactivate(self):
        if self.is_active:
            self.is_active = False
            print(f"{self.name} deactivated, consuming 0W")
            
    def get_consumption(self):
        if self.is_active:
            return self.power_consumption
        else:
            return 0.0


