def taipei_101():
    # Taipei 101 coordinates (simplified)
    # Unit: centimeters
    bottom_base = [(-4000, 0), (4000, 0), (2500, 10800), (-2500, 10800)]
    plate = [(-3000, 10800), (3000, 10800), (3000, 11250), (-3000, 11250)]

    knots = []
    for i in range(8):
        y_base = 11250 + i * 3600
        knots.append([(-2500, y_base), (2500, y_base), (3500, y_base + 3600), (-3500, y_base + 3600)])

    top_spire = [(-1500, 40050), (1500, 40050), (2000, 45450), (-2000, 45450)]
    damper = [(-1000, 45450), (1000, 45450), (700, 47700), (-700, 47700)]
    lightning_rod = [(-200, 47700), (200, 47700), (50, 50800), (-50, 50800)]
    return [
        bottom_base,
        plate,
        *knots,
        top_spire,
        damper,
        lightning_rod,
    ]


def taipei_101_2():
    shape = []
    y = 0

    def add_level(width_bottom, width_top, height):
        nonlocal y
        shape_index = int(len(shape) * 0.5)
        shape.insert(shape_index, (-width_bottom // 2, y))
        shape.insert(shape_index, (-width_top // 2, y + height))
        shape.insert(shape_index, (width_top // 2, y + height))
        shape.insert(shape_index, (width_bottom // 2, y))
        y += height

    add_level(8000, 5000, 10800)  # Bottom base
    add_level(6000, 6000, 450)  # Plate
    for _ in range(8):
        add_level(5000, 7000, 3600)  # Knots
    add_level(3000, 4000, 5400)  # Top spire
    add_level(2000, 1400, 2250)  # Damper
    add_level(400, 100, 3100)  # Lightning rod
    return [shape]
