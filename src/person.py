class Person:
    def __init__(self, first, last, robotics, next_steps, t_leader, car):
        self.first = first
        self.last = last
        self.robotics = 1 if robotics == "Yes" else 0
        self.next_steps = 1 if next_steps == "Yes" else 0
        self.t_leader = 1 if t_leader == "Yes" else 0
        self.car = 0 if car == "" else (4 if car == "4 or more" else car)  # "" means 0, "4 or more" means 4
