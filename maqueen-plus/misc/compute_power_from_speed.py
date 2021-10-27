
points = [
    (20, 0),
    (40, 440),
    (50, 590),
    (60, 680),
    (80, 840),
    (100, 900),
    (150, 1010),
    (255, 1100)
]

def linear_coefficients(xA, xB, yA, yB):
    delta_x = xB - xA
    delta_y = yB - yA
    
    m = (delta_y) / delta_x
    h = yA - xA*m
    
    return m, h

for i in range(0, len(points)-1):
    xA, yA = points[i]
    xB, yB = points[i+1]
    
    m, y = linear_coefficients(xA, xB, yA, yB)
    
    print(1/m, -y/m)
    

    
    
