from pulp import LpMinimize, LpProblem, LpVariable
 

def model():
    func = LpProblem("Problema", LpMinimize)

    x1 = LpVariable("x1", lowBound=0)
    y1 = LpVariable("y1", lowBound=0)
    x2 = LpVariable("x2", lowBound=0)
    y2 = LpVariable("y2", lowBound=0)
    x3 = LpVariable("x3", lowBound=0)
    y3 = LpVariable("y3", lowBound=0)
    x4 = LpVariable("x4", lowBound=0)
    y4 = LpVariable("y4", lowBound=0)
    x5 = LpVariable("x5", lowBound=0)
    y5 = LpVariable("y5", lowBound=0)

    func += 2000*(x1 + x2 + x3 + x4 + x5) + 1000*(y1 + y2 + y3 + y4 + y5), "Función objetivo"

    func += 160*x1 - 50*y1 >= 6000, "C1"
    func += 160*x2 - 50*y2 >= 7000, "C2"
    func += 160*x3 - 50*y3 >= 8000, "C3"
    func += 160*x4 - 50*y4 >= 9500, "C4"
    func += 160*x5 - 50*y5 >= 11000, "C5"
    func += x1 == 50, "C6"
    func += x2 == x1*0.95 + y1, "C7"
    func += x3 == x2*0.95 + y2, "C8"
    func += x4 == x3*0.95 + y3, "C9"
    func += x5 == x4*0.95 + y4, "C10"

    func.solve()

    print("Status:", func.status)
    print("Optimal Solution:")

    vars = [x1,x2,x3,x4,x5,y1,y2,y3,y4,y5]
    vare = []
    for i in vars:
        vare.append(i.value())
        print(f"{i} = {i.value()}")

    print("Optimal Value of Objective Function:", func.objective.value())

    return vare, func
