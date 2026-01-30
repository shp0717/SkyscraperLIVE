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
