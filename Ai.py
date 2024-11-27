import random

# Define the parameter ranges and options for a coffee recipe
parameters = {
    "beans": ["Arabica", "Robusta"],
    "roast": ["light", "meium", "dark"],
    "grind_size": ["extra fine","fine","fine-medium", "medium","medium-coarse", "coarse", "extra coarse"],
    "water_ratio": (10, 20),  # grams of water per gram of coffee
    "temperature": (80, 100),  # degrees Celsius
    "brewing_time": (1, 10),  # minutes
    "additives": ["milk", "sugar","caramel syrup", "vanilla syrup"],
}

# Function to generate a random coffee recipe
def generate_random_recipe():
    return {
        "beans": random.choice(parameters["beans"]),
        "roast": random.choice(parameters["roast"]),
        "grind_size": random.choice(parameters["grind_size"]),
        "water_ratio": round(random.uniform(*parameters["water_ratio"]), 2),
        "temperature": round(random.uniform(*parameters["temperature"]), 2),
        "brewing_time": round(random.uniform(*parameters["brewing_time"]), 2),
        "additives": {add: round(random.uniform(0, 30), 2) for add in parameters["additives"]}  # Random additive proportions
    }

# Fitness function based on user rating
def fitness(recipe):
    """
    Prompt the user to rate the given recipe on a scale of 0 to 10.
    """
    print("\nEvaluate the following coffee recipe:")
    print(f"Beans: {recipe['beans']}")
    print(f"roast: {recipe['roast']}")
    print(f"Grind Size: {recipe['grind_size']}")
    print(f"Water Ratio: {recipe['water_ratio']} grams of water per gram of coffee")
    print(f"Temperature: {recipe['temperature']}°C")
    print(f"Brewing Time: {recipe['brewing_time']} minutes")
    print("Additives:")
    for add, qty in recipe['additives'].items():
        print(f"  - {add}: {qty} ml/grams")
    
    while True:
        try:
            rating = float(input("Rate this recipe on a scale of 0 to 10: "))
            if 0 <= rating <= 10:
                return rating
            else:
                print("Please enter a number between 0 and 10.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Crossover function to combine two parent recipes
def crossover(parent1, parent2):
    """
    Mixes two recipes to create an offspring recipe.
    """
    child = {}
    for key in parent1:
        if key == "additives":
            # Handle additives separately
            child[key] = {
                add: (parent1[key][add] + parent2[key][add]) / 2
                for add in parent1[key]
            }
        elif isinstance(parent1[key], (int, float)):
            # Take the average for numerical values
            child[key] = (parent1[key] + parent2[key]) / 2
        else:
            # Randomly inherit categorical attributes
            child[key] = random.choice([parent1[key], parent2[key]])
    return child

# Mutation function to randomly alter a recipe
def mutate(recipe, mutation_rate=0.1):
    """
    Randomly modifies parts of a recipe based on the mutation rate.
    """
    for key in recipe:
        if key == "additives":
            for add in recipe[key]:
                if random.random() < mutation_rate:
                    recipe[key][add] += random.uniform(-2, 2)  # Small change
                    recipe[key][add] = max(0, recipe[key][add])  # Ensure non-negative
        elif key in ["water_ratio", "temperature", "brewing_time"]:
            if random.random() < mutation_rate:
                change = random.uniform(-1, 1)
                recipe[key] += change
                # Clamp values within valid ranges
                recipe[key] = max(parameters[key][0], min(parameters[key][1], recipe[key]))
        elif key in ["beans", "grind_size","roast"]:
            if random.random() < mutation_rate:
                recipe[key] = random.choice(parameters[key])
    return recipe

# Evolutionary algorithm
def evolutionary_algorithm(population_size=10, generations=5, mutation_rate=0.1):
    # Initialize the population with random recipes
    population = [generate_random_recipe() for _ in range(population_size)]
    
    for generation in range(generations):
        print(f"\n=== Generation {generation + 1} ===")
        # Evaluate fitness for the population
        fitness_scores = [(recipe, fitness(recipe)) for recipe in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)  # Sort by fitness
        
        # Print the best recipe of the generation
        print(f"\nBest Recipe of Generation {generation + 1}:")
        best_recipe, best_score = fitness_scores[0]
        print(f"Score: {best_score:.2f}")
        print(best_recipe)
        
        # Selection: Keep the top half of the population
        selected = [fs[0] for fs in fitness_scores[:len(fitness_scores)//2]]
        
        # Crossover and mutation to refill the population
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected, 2)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        # Update the population
        population = new_population
    
    # Return the best recipe from the final generation
    best_recipe = max(population, key=fitness)
    print("\nOptimal Coffee Recipe Found:")
    print(best_recipe)
    return best_recipe

# Main program to run the optimizer
if __name__ == "__main__":
    print("Welcome to the Coffee Recipe Optimizer!")
    print("You will be asked to rate recipes during the optimization process.")
    
    try:
        generations = int(input("Enter the number of generations to run (default is 50): ") or 50)
        best_recipe = evolutionary_algorithm(population_size=10, generations=generations, mutation_rate=0.2)
    except ValueError:
        print("Invalid input. Using default of 50 generations.")
        best_recipe = evolutionary_algorithm(population_size=10, generations=50, mutation_rate=0.2)
    
    print("\nThank you for participating! The best recipe is:")
    print(best_recipe)
