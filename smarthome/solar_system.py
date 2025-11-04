STATUS_IDLE = "idle"
STATUS_GENERATING = "generating"
STATUS_CHARGING = "charging"

class SolarSystem:
    def __init__(self, capacity, battery_level=0.0, generation_rate=0.0):
        """
        capacity: battery capacity in kWh
        battery_level: initial stored energy in kWh (default 0.0)
        generation_rate: last computed generation rate in Watts (default 0.0)
        """
        self.battery_capacity = float(capacity)      # kWh
        self.battery_level = float(battery_level)    # kWh
        self.generation_rate = float(generation_rate)  # W
        self.status = STATUS_IDLE

    def generate_power(self, sun_intensity):
        """
        Compute instantaneous solar power (W) from a sun_intensity scale (0-10).
        Returns generation rate in Watts.
        """
        max_power = 5000  # W (peak)
        self.generation_rate = max_power * (float(sun_intensity) / 10.0)
        self.status = STATUS_GENERATING
        print(f"Solar system generating {self.generation_rate:.1f} W")
        return self.generation_rate

    def charge_battery(self, power_input_w, duration_hours=1.0):
        """
        Charge battery with given input power (W) over duration_hours.
        Converts power -> energy: energy_kwh = power_w * hours / 1000.
        Updates battery_level (kWh) and returns leftover power in W (that could not be stored),
        expressed as equivalent continuous Watts over the same duration_hours.
        """
        if power_input_w <= 0 or duration_hours <= 0:
            print("No charging: non-positive power or duration.")
            return 0.0

        energy_input_kwh = (power_input_w * float(duration_hours)) / 1000.0
        available_capacity_kwh = max(0.0, self.battery_capacity - self.battery_level)
        energy_stored_kwh = min(energy_input_kwh, available_capacity_kwh)

        self.battery_level += energy_stored_kwh
        # clamp and round for readability
        self.battery_level = round(min(self.battery_level, self.battery_capacity), 3)

        self.status = STATUS_CHARGING if energy_stored_kwh > 0 else STATUS_IDLE
        print(f"Battery level: {self.battery_level:.3f}/{self.battery_capacity:.3f} kWh (stored {energy_stored_kwh:.3f} kWh)")

        leftover_energy_kwh = energy_input_kwh - energy_stored_kwh
        # convert leftover energy back to equivalent continuous Watts over duration_hours
        leftover_power_w = (leftover_energy_kwh * 1000.0) / float(duration_hours) if duration_hours > 0 else 0.0
        return leftover_power_w

    def supply_power(self, power_needed_w, duration_hours=1.0):
        """
        Supply up to power_needed_w (W) over duration_hours from the battery.
        Returns the actual power supplied in Watts (over the same continuous duration).
        """
        if power_needed_w <= 0 or duration_hours <= 0:
            return 0.0

        energy_needed_kwh = (power_needed_w * float(duration_hours)) / 1000.0
        energy_from_batt_kwh = min(energy_needed_kwh, self.battery_level)

        self.battery_level -= energy_from_batt_kwh
        self.battery_level = round(max(self.battery_level, 0.0), 3)

        power_supplied_w = (energy_from_batt_kwh * 1000.0) / float(duration_hours) if duration_hours > 0 else 0.0
        if power_supplied_w > 0:
            print(f"Supplying {power_supplied_w:.1f} W from battery ({energy_from_batt_kwh:.3f} kWh over {duration_hours} h).")
        else:
            print("Battery empty or no power requested.")
        return power_supplied_w