class Car():
    def __init__(self,brand,speed):
        self.brand = brand
        self.speed = speed
    def accelerate(self):
        self.speed += 10
    def brake(self):
        self.speed -= 10
    def __repr__(self):
        return f'<Car brand={self.brand} speed={self.speed}>'

class ElectricCar(Car):
    def __init__(self, brand, speed, battery):
        super().__init__(brand, speed)
        self.battery = battery
    def charge(self):
        self.battery = 100
    def accelerate(self):
        super().accelerate()
        self.battery -= 10
    def __repr__(self):
        return f'<Car brand={self.brand} speed={self.speed} battery={self.battery}>'

cars = []
car_specs = {
    'toyota':100,
    'mazda':120,
    'audi':40,
    'ferrari':300,
    'hyundai':110
}

for car_brand in car_specs:
    car_object = ElectricCar(car_brand, car_specs[car_brand], 100)
    cars.append(car_object)

print('before accelerating:')
for car in cars:
    print(car)

for car in cars:
    car.accelerate()

print('after accelerating:')
for car in cars:
    print(car)
