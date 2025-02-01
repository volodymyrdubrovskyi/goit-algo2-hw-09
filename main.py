import random
import math

# Визначення функції Сфери
def sphere_function(x):
    return sum(xi ** 2 for xi in x)

# Функція для визначення сусідів поточної точки
def get_neighbors(current, step_size=0.1):
    x, y = current
    return [
        (x + step_size, y),
        (x - step_size, y),
        (x, y + step_size),
        (x, y - step_size)
    ]
    
# Hill Climbing
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    current_point = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(len(bounds))]
    current_value = func(current_point)

    for iteration in range(iterations):
        neighbors = get_neighbors(current_point)
        # Пошук найкращого сусіда
        next_point = None
        next_value = float('inf')
        for neighbor in neighbors:
            value = func(neighbor)
            if value < next_value:
                next_point = neighbor
                next_value = value
        # Якщо не вдається знайти кращого сусіда — зупиняємось
        if abs(next_value - current_value) < epsilon:
            break
        # Переходимо до кращого сусіда
        current_point, current_value = next_point, next_value
    return current_point, current_value

# Random Local Search
def random_local_search(func, bounds, iterations=1000, step_size=0.5, probability=0.2, epsilon=1e-6):
    current_point = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(len(bounds))]
    current_value = func(current_point)
    for iteration in range(iterations):
        new_point = [max(min(x + random.uniform(-step_size, step_size), b[1]), b[0]) for x, b in zip(current_point, bounds)]
        new_value = func(new_point)
        if new_value < current_value or random.random() < probability:
            if abs(current_value - new_value) < epsilon:
                break
            current_point, current_value = new_point, new_value
    return current_point, current_value

# Simulated Annealing
def simulated_annealing(func, bounds, temperature=1000, cooling_rate=0.95, step_size=1, epsilon=1e-6):
    current_solution = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(len(bounds))]
    current_energy = func(current_solution)
    best_solution = current_solution[:]
    best_energy = current_energy

    while temperature > epsilon:
        new_solution = []
        for i in range(len(bounds)):
            new_value = current_solution[i] + random.uniform(-step_size, step_size)
            new_value = max(min(new_value, bounds[i][1]), bounds[i][0])
            new_solution.append(new_value)
        new_energy = func(new_solution)
        delta_energy = new_energy - current_energy

        if delta_energy < 0 or random.random() < math.exp(-delta_energy / temperature):
            current_solution = new_solution[:]
            current_energy = new_energy

            if new_energy < best_energy:
                best_solution = new_solution[:]
                best_energy = new_energy

        temperature *= cooling_rate

        if temperature < epsilon:
            break

    return best_solution, best_energy

if __name__ == "__main__":
    bounds = [(-5, 5), (-5, 5)]

    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print("Розв'язок:", hc_solution, "Значення:", hc_value)

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print("Розв'язок:", rls_solution, "Значення:", rls_value)

    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print("Розв'язок:", sa_solution, "Значення:", sa_value)
