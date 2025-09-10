from solar_system import SolarSystem

class Home:
    def __init__(self, solar_capacity):
        self.solar_system = SolarSystem(capacity=solar_capacity)
        self.device = {}
        self.total_consumption_wats = 0.0
        self.total_grid_import_kwh = 0.0
        self.total_solar_usage_kwh = 0.0
        
    def add_device(self, device):
        self.device[device.name] = device
        print(f"Added device: {device.name}")
        
    def get_total_consumption(self):
        total = 0
        for device in self.device.values():
            total += device.get_consumption()
        self.total_consumption_wats = total
        return total
    
    def run_simulation(self, sun_intensity, duration_hours):
        current_demand = self.get_total_consumption()
        solar_power = self.solar_system.generate_power(sun_intensity)
        power_to_use = min(current_demand, solar_power)
        remaining_demand = current_demand - power_to_use
        self.total_solar_usage_kwh += (power_to_use * duration_hours) / 1000.0
        surplus_power = solar_power - power_to_use
        self.solar_system.charge_battery(surplus_power)
        power_from_battery = self.solar_system.supply_power(remaining_demand)
        remaining_demand -= power_from_battery
        if remaining_demand > 0:
            self.total_grid_import_kwh += (remaining_demand * duration_hours) / 1000.0
            print(f"Drawing {remaining_demand}W from grid.")
            
# Note: self.battery_level is in kWh
