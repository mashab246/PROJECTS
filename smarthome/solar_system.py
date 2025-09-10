STATUS_IDLE = "idle"
STATUS_GENERATING = "generating"
STATUS_CHARGING = "charging"

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