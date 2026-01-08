from solar_system import SolarSystem

class Home:
    def __init__(self, solar_battery_capacity):
        self.solar_system = SolarSystem(solar_battery_capacity)
        self.device = {}
        self.total_consumption_watts = 0.0
        self.total_grid_import_kwh = 0.0
        self.total_solar_usage_kwh = 0.0
        
    def add_device(self, device):
        self.device[device.name] = device
        return(f"Added device: {device.name}")
        
    def calculate_total_consumption(self):
        """Calculate total power demand from all active devices."""
        total = 0.0
        for device in self.device.values():
            total += device.get_consumption()
            
        self.total_consumption_wats = total
        return total
    
    def run_simulation(self, sun_intensity, duration_hours):
        """Simulate energy usage for a given time period."""
        current_demand = self.calculate_total_consumption()
        
        #solar generation
        solar_power = self.solar_system.generate_power(sun_intensity)
        
        solar_power_used = min(current_demand, solar_power)

        remaining_demand = current_demand - solar_power_used
        
        self.total_solar_usage_kwh += (solar_power_used * duration_hours) / 1000.0
        
        #store excess solar energy
        excess_solar_power = solar_power - solar_power_used
        
        self.solar_system.store_energy(excess_solar_power, duration_hours)
        
        #use battery
        battery_power = self.solar_system.supply_power(remaining_demand)
        remaining_demand -= battery_power
        
        #remaining demand comes from grid
        if remaining_demand > 0:
            self.total_grid_import_kwh += (remaining_demand * duration_hours) / 1000.0
            return(f"Drawing {remaining_demand}W from grid.")
            
# Note: self.battery_level is in kWh
