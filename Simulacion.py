
import time
import random

class Vehicle:
    def __init__(self, id, position, destination):
        self.id = id
        self.position = position
        self.destination = destination
        self.movements = 0
        self.completed = False
        self.red_light_stops = 0
        self.start_time = time.time()

    def update_position(self, traffic_lights):
        if self.position != self.destination:
            # Comprobar semáforos en la posición del vehículo
            for light in traffic_lights:
                if light.position == self.position:
                    if light.state == 'red':
                        self.red_light_stops += 1
                        return  # Detener el vehículo si el semáforo está en rojo

            # Mover el vehículo hacia el destino si no está detenido
            if self.position[0] < self.destination[0]:
                self.position = (self.position[0] + 1, self.position[1])
            elif self.position[0] > self.destination[0]:
                self.position = (self.position[0] - 1, self.position[1])
            elif self.position[1] < self.destination[1]:
                self.position = (self.position[0], self.position[1] + 1)
            elif self.position[1] > self.destination[1]:
                self.position = (self.position[0], self.position[1] - 1)

            self.movements += 1

            # Verificar si el vehículo ha llegado al destino
            if self.position == self.destination:
                self.completed = True
                self.end_time = time.time()

    def get_time_taken(self):
        if self.completed:
            return self.end_time - self.start_time
        return None

class TrafficLight:
    def __init__(self, position):
        self.position = position
        self.state = 'red'
        self.change_time = 3  # Tiempo de cambio de semáforo
        self.last_change = time.time()

    def update(self, current_time):
        # Cambiar de estado si ha pasado el tiempo suficiente
        if current_time - self.last_change >= self.change_time:
            self.state = 'green' if self.state == 'red' else 'red'
            self.last_change = current_time

# La simulación y la adición de vehículos y semáforos siguen siendo las mismas.
class Simulation:
    def __init__(self, max_time):
        self.vehicles = []
        self.traffic_lights = []
        self.max_time = max_time

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def add_traffic_light(self, traffic_light):
        self.traffic_lights.append(traffic_light)

    def run(self):
        start_time = time.time()  # Tiempo de inicio global de la simulación
        time_step = 0.1  # Intervalo de tiempo para cada actualización
        current_time = start_time
        
        while current_time - start_time < self.max_time:
            # Actualizar semáforos
            for light in self.traffic_lights:
                light.update(current_time)

            # Actualizar posiciones de vehículos
            for vehicle in self.vehicles:
                vehicle.update_position(self.traffic_lights)

            # Incrementar el tiempo
            current_time += time_step
            time.sleep(time_step)

        # Imprimir el resultado de la simulación
        for vehicle in self.vehicles:
            print(f"Vehicle {vehicle.id}:")
            print(f"  Final Position: {vehicle.position}")
            print(f"  Movements: {vehicle.movements}")
            print(f"  Completed: {vehicle.completed}")
            print(f"  Red Light Stops: {vehicle.red_light_stops}")
            print(f"  Time Taken: {vehicle.get_time_taken()} seconds")

        # Imprimir el estado de los semáforos
        for light in self.traffic_lights:
            print(f"Traffic Light at {light.position}: {light.state}")

# Inicializar la simulación
simulation = Simulation(max_time=20)

# Crear vehículos
for i in range(5):
    initial_position = (random.randint(0, 10), random.randint(0, 10))
    destination = (random.randint(0, 10), random.randint(0, 10))
    vehicle = Vehicle(id=i + 1, position=initial_position, destination=destination)
    simulation.add_vehicle(vehicle)

# Crear semáforos en posiciones de intersección potencial
for i in range(4):
    traffic_light = TrafficLight(position=(random.randint(0, 10), random.randint(0, 10)))
    simulation.add_traffic_light(traffic_light)

# Ejecutar la simulación
simulation.run()
