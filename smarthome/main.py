from smarthome.shems import EnergyConsumer, Light, HVAC, Appliance, SolarSystem, Home

print("----Smart Home Energy Management System Simulation----")
my_home = Home(solar_capacity= 10.0)  # 10 kWh battery capacity

print("\n--Adding Devices--")
living_room_light = Light(name= "Living Room Light", max_consumption = 60.0)
kitchen_hvac = HVAC(name= "Kitchen HVAC", power_consumption = 3500.0, current_temp = 25.0)
washing_machine = Appliance(name= "Washing Machine", power_consumption = 2000.0)

my_home.add_device(living_room_light)
my_home.add_device(kitchen_hvac)
my_home.add_device(washing_machine)

print("\n--Simulating Morning(Cloudy) --")
living_room_light.set_brightness(0.8)  # 80% brightness
kitchen_hvac.set_target_temp(22.0)  # Set target temp to 22°C

my_home.run_simulation(sun_intensity = 0, time_delta_hours = 4)  # 4 hours of cloudy weather

print("\n--Simulating Afternoon(Sunny) --")
washing_machine.start_cycle("normal")
living_room_light.set_brightness(0.0)  # Turn off light

my_home.run_simulation(sun_intensity = 10, time_delta_hours = 4)  # 4 hours of sunny weather

print("\n--Simulating Evening (Battery Use) --")
washing_machine.stop_cycle()

my_home.run_simulation(sun_intensity = 0, time_delta_hours = 4)  # 4 hours of evening   

print("\n---Final Report---")
print(f"Total Energy Consumed: {my_home.total_grid_import_kwh:.2f} Wh")
print(f"Total Solar Energy Used: {my_home.total_solar_usage_kwh:.2f} Wh")
print(f"Final Battery Level: {my_home.solar_system.battery_level:.2f} Wh")

