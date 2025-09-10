STATUS_IDLE = "idle"
STATUS_GENERATING = "generating"
STATUS_CHARGING = "charging"

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
        
class Light(EnergyConsumer):
    def __init__(self, name, power_consumption):
        super().__init__(name, power_consumption)
        self.original_power_consumption = power_consumption
        self.brightness_level = 0
        
    def set_brightness(self, level):
        self.brightness_level = max(0, min(1.0, level))
        if self.brightness_level > 0:
            self.activate()
            self.power_consumption = self.original_power_consumption * self.brightness_level
        else:
            self.deactivate()
            self.power_consumption = 0
            
        print(f"{self.name} brightness set to {self.brightness_level * 100}%")
        
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
                
class Appliance(EnergyConsumer):
    def __init__(self, name, power_consumption):
        super().__init__(name, power_consumption)
        self.status = None
        self.available_cycles = ["normal", "eco", "intensive"]
        self.current_cycle = None
        
    def start_cycle(self, cycle_name):
        if cycle_name in self.available_cycles:
            self.current_cycle = cycle_name
            self.status = "running"
            self.activate()
            print(f"Starting {self.current_cycle} cycle on {self.name}.")
        else:
            print(f"Error: Cycle {cycle_name} not available for cycle.")
            
    def stop_cycle(self):
        if self.status == "running":
            self.status = "stopped"
            self.deactivate()
            print(f"{self.name} cycle stopped.")
            
class SolarSystem:
    def __init__(self, capacity):
        self.battery_capacity = capacity
        self.battery_level = 0
        self.generation_rate = 0
        self.status = "idle"
        
    def generate_power(self, sun_intensity):
        max_power = 5000
        self.generation_rate = max_power * (sun_intensity / 10.0)
        self.status = "generating"
        print(f"Solar system generating {self.generation_rate}W")
        return self.generation_rate
    
    def charge_battery(self, power_input):
        if power_input < 0:
            print("Error: Cannot charge battery with negative power input.")
            return 0
        charge_added = min(power_input, self.battery_capacity - self.battery_level)
        self.battery_level += charge_added
        self.status = "charging"
        print(f"Battery level is now at {self.battery_level}/{self.battery_capacity}Wh")
        return power_input - charge_added
    
    def supply_power(self, power_needed):
        power_from_battery = min(power_needed, self.battery_level * 1000)
        self.battery_level -= power_from_battery / 1000
        self.battery_level = round(self.battery_level, 2)
        print(f"Supplying {power_from_battery}W from battery.")
        return power_from_battery
    
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
