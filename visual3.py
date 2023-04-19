import pygame
import random
import math
# Define the window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define the parameters for the simulation
NUM_CREATURES = 500
MUTATION_RATE = 0.1
MAX_SPEED = 5

# Define the Creature class
class Creature(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(1, MAX_SPEED)
        self.direction = random.uniform(0, 359)
        self.color = RED
        self.health = 100
        self.age = 0
    
    def update(self):
        # Move the creature in its current direction and at its current speed
        dx = self.speed * math.cos(self.direction)
        dy = self.speed * math.sin(self.direction)
        self.rect.x += dx
        self.rect.y += dy
        
        # If the creature goes off the screen, wrap it around to the other side
        if self.rect.x < 0:
            self.rect.x = WINDOW_WIDTH
        elif self.rect.x > WINDOW_WIDTH:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = WINDOW_HEIGHT
        elif self.rect.y > WINDOW_HEIGHT:
            self.rect.y = 0
        
        # Decrease the creature's health every frame
        self.health -= 1
        
        # If the creature's health reaches zero, it dies
        if self.health <= 0:
            self.kill()
        
        # Increase the creature's age every frame
        self.age += 1
        
        # Mutate the creature's color randomly
        if random.random() < MUTATION_RATE:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def reproduce(self):
        # Create a new creature that is a copy of this one
        child = Creature(self.rect.x, self.rect.y)
        child.speed = self.speed
        child.direction = self.direction
        child.color = self.color
        child.health = 100
        
        # Mutate the child's speed and direction randomly
        if random.random() < MUTATION_RATE:
            child.speed = random.randint(1, MAX_SPEED)
        if random.random() < MUTATION_RATE:
            child.direction = random.uniform(0, 2 * math.pi)
        
        # Return the child creature
        return child

# Initialize Pygame
pygame.init()

# Set up the window
screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption("Biological Evolution")

# Create a group for all the creatures
creature_group = pygame.sprite.Group()

# Create the initial population of creatures
for i in range(NUM_CREATURES):
    creature = Creature(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
    creature_group.add(creature)

# Run the simulation
clock = pygame.time.Clock()
generation = 1
while True:
    # Handle events
    for event in pygame.event.get():
        # If the user closes the window, quit the program
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        # If the user presses the space bar, create a new generation of creatures
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Calculate the average age and health of the current generation
            total_age = 0
            total_health = 0
            for creature in creature_group:
                total_age += creature.age
                total_health += creature.health
            average_age = total_age / NUM_CREATURES
            average_health = total_health / NUM_CREATURES
            
            # Print the statistics for the current generation
            print("Generation:", generation)
            print("Average Age:", round(average_age, 2))
            print("Average Health:", round(average_health, 2))
            
            # Create a new group for the next generation of creatures
            next_generation = pygame.sprite.Group()
            
            # Keep the best creature from the previous generation
            best_creature = max(creature_group, key=lambda c: c.health)
            next_generation.add(best_creature)
            
            # Create the rest of the creatures in the next generation by reproducing
            while len(next_generation) < NUM_CREATURES:
                # Select two random parents from the previous generation
                parent1 = random.choice(list(creature_group))
                parent2 = random.choice(list(creature_group))
                
                # Make sure the parents are not the same creature
                while parent2 == parent1:
                    parent2 = random.choice(list(creature_group))
                
                # Reproduce the parents and add the child to the next generation
                child = parent1.reproduce()
                next_generation.add(child)
                
                # If there is room for another child, reproduce the parents in the opposite order
                if len(next_generation) < NUM_CREATURES:
                    child = parent2.reproduce()
                    next_generation.add(child)
            
            # Replace the current generation with the next generation
            creature_group = next_generation
            
            # Increment the generation counter
            generation += 1
    
    # Clear the screen
    screen.fill(WHITE)
    
    # Update and draw all the creatures
    creature_group.update()
    creature_group.draw(screen)
    
    # Update the display
    pygame.display.update()
    
    # Wait for a short  amount of time to control the frame rate
    clock.tick(50)

# Quit Pygame
pygame.quit()
quit()
