class SolarSystem:
    def __init__(self, battery_capacity_kwh):
       #Handles solar power generation and battery storage.
        self.battery_capacity = float(battery_capacity_kwh)      # kWh
        self.battery_level = 0.0    # kWh

    def generate_power(self, sun_intensity):
        """
        Generate solar power in Watts.
        sun_intensity must be between 0.0 and 1.0
        """
        sun_intensity = max(0.0, min(1.0, float(sun_intensity)))
        max_power_watts = 5000
        return max_power_watts * sun_intensity

    def store_battery(self, power_watts, duration_hours):
        """
        Store energy in the battery.
        Returns unused energy in kWh.
        """

        energy_kwh = (power_watts * duration_hours) / 1000.0
        free_space = self.battery_capacity - self.battery_level

        stored = min(energy_kwh, free_space)
        self.battery_level += stored

        return energy_kwh - stored
    
    def supply_power(self, power_needed_watts, duration_hours):
        """
        Supply energy from the battery.
        Returns power supplied in Watts.
        """
        energy_needed = (power_needed_watts * duration_hours) / 1000.0
        energy_given = min(energy_needed, self.battery_level)

        self.battery_level -= energy_given

        return (energy_given * 1000.0) / duration_hours