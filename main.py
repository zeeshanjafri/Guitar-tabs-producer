import pygame

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 1000  # Increased width to show more notes
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Guitar Tabs Producer")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font setup
font = pygame.font.SysFont('Arial', 24)

# Example tab data - each inner list represents a string (high E to low E)
# 0 means open string, numbers 1-20 represent frets
example_tab = [
    [0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # High E string
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # B string
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # G string
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # D string
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A string
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # Low E string
]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the tab lines
    line_spacing = 40
    start_y = 100
    for i in range(6):  # 6 strings for guitar
        y = start_y + (i * line_spacing)
        pygame.draw.line(screen, BLACK, (100, y), (900, y), 2)

    # Draw string names
    string_names = ["e", "B", "G", "D", "A", "E"]
    for i, name in enumerate(string_names):
        text_surface = font.render(name + "|", True, BLACK)
        screen.blit(text_surface, (70, start_y + (i * line_spacing) - 20))

    # Draw the tab numbers
    note_spacing = 50  # Space between each note
    for string_idx, string_notes in enumerate(example_tab):
        for note_idx, fret in enumerate(string_notes):
            if fret > 0:  # Only draw if there's a note (not 0)
                x = 100 + (note_idx * note_spacing)
                y = start_y + (string_idx * line_spacing) - 20
                text_surface = font.render(str(fret), True, BLACK)
                screen.blit(text_surface, (x, y))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit() 