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

# Функція для визначення випадкового сусіда
def get_random_neighbor(current, bounds, step_size=0.5):
    return [max(min(x + random.uniform(-step_size, step_size), b[1]), b[0]) for x, b in zip(current, bounds)]

# Random Local Search
def random_local_search(func, bounds, iterations=1000, step_size=0.5, probability=0.2, epsilon=1e-6):
    current_point = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(len(bounds))]
    current_value = func(current_point)
    for iteration in range(iterations):
        # Отримання випадкового сусіда
        new_point = get_random_neighbor(current_point, bounds, step_size)
        new_value = func(new_point)
        # Перевірка умови переходу
        if new_value < current_value or random.random() < probability:
            if abs(current_value - new_value) < epsilon:
                break
            current_point, current_value = new_point, new_value
    return current_point, current_value

# Функція для генерації сусіда
def generate_neighbor(solution):
    x, y = solution
    new_x = x + random.uniform(-2, 2)
    new_y = y + random.uniform(-2, 2)
    # Перевірка меж
    new_x = max(min(new_x, 5), -5)
    new_y = max(min(new_y, 5), -5)
    return (new_x, new_y)

# Simulated Annealing
def simulated_annealing(func, initial_solution, temperature, cooling_rate, epsilon=1e-6):
    current_solution = initial_solution
    current_energy = func(current_solution)
    best_solution = current_solution
    best_energy = current_energy
    while temperature > epsilon:
        new_solution = generate_neighbor(current_solution)
        new_energy = func(new_solution)
        delta_energy = new_energy - current_energy
        if delta_energy < 0 or random.random() < math.exp(-delta_energy / temperature):
            current_solution = new_solution
            current_energy = new_energy
            if new_energy < best_energy:
                best_solution = new_solution
                best_energy = new_energy
        temperature *= cooling_rate
    return best_solution, best_energy

if __name__ == "__main__":
    # Межі для функції
    bounds = [(-5, 5), (-5, 5)]

    # Генеруємо початкове рішення для імітації відпалу
    initial_solution = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(len(bounds))]

    # Виконання алгоритмів
    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print("Розв'язок:", hc_solution, "Значення:", hc_value)

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print("Розв'язок:", rls_solution, "Значення:", rls_value)

    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(
        sphere_function,
        initial_solution,
        temperature=1000,
        cooling_rate=0.95
    )
    print("Розв'язок:", sa_solution, "Значення:", sa_value)
