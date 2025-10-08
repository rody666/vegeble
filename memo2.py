class Car:
    def __init__(self,brand,speed):
        self.brand = brand
        self.speed = speed
    def accelerate(self):
        self.speed += 10
    def brake(self):
        self.speed -= 10
    def __repr__(self):
        return f'<Car brand={self.brand} speed={self.speed}>'
