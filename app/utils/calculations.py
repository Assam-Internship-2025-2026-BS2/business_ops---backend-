def calculate_dropoff(previous, current):

    if previous == 0:
        return 0

    drop = ((previous - current) / previous) * 100

    return round(drop,2)