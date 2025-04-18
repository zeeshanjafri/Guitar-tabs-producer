import pygame
import requests
import json
from typing import List, Dict
import os
from urllib.parse import quote

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Guitar Tabs Producer")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Font setup
font = pygame.font.SysFont('Arial', 24)
input_font = pygame.font.SysFont('Arial', 20)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = input_font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = BLUE if self.active else BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = input_font.render(self.text, True, self.color)
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

def fetch_song_from_songsterr(song_name: str) -> Dict:
    """Fetch song data from Songsterr API"""
    try:
        print(f"\nSong requested - {song_name}")
        
        # Format the song name for the URL
        formatted_song_name = song_name.lower().replace(' ', '+')
        search_url = f"https://www.songsterr.com/a/wa/s={formatted_song_name}"
        print(f"Request URL: {search_url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        search_response = requests.get(search_url, headers=headers, allow_redirects=True)
        print(f"Response status code: {search_response.status_code}")
        
        if search_response.status_code == 200:
            print("API response received successfully")
            
            # Save the response to a file
            file_path = os.path.join(os.getcwd(), 'songsterr_api_response.txt')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(search_response.text)
            print(f"API response saved to: {file_path}")
            
            # TODO: Parse the HTML response to extract tab data
            return {"status": "success", "url": search_response.url}
        else:
            print(f"Error: API request failed with status code {search_response.status_code}")
            print(f"Response content: {search_response.text}")
        return None
    except Exception as e:
        print(f"Error fetching song: {str(e)}")
        return None

# Create input box
input_box = InputBox(100, 50, 200, 32)

# Main game loop
running = True
current_tab = [[-1 for _ in range(16)] for _ in range(6)]  # Initialize empty tab

print("Guitar Tabs Producer started. Enter a song name in the input box.")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        # Handle input box events
        song_name = input_box.handle_event(event)
        if song_name:
            song_data = fetch_song_from_songsterr(song_name)
            if song_data:
                print("Song data received and saved to songsterr_api_response.txt")
                # TODO: Parse the song data and update current_tab
                print("GUI updated with new tab data")

    # Clear the screen
    screen.fill(WHITE)

    # Draw input box
    input_box.draw(screen)
    
    # Draw "Enter song name:" label
    label = font.render("Enter song name:", True, BLACK)
    screen.blit(label, (100, 20))

    # Draw the tab lines
    line_spacing = 40
    start_y = 150
    for i in range(6):  # 6 strings for guitar
        y = start_y + (i * line_spacing)
        pygame.draw.line(screen, BLACK, (100, y), (900, y), 2)

    # Draw string names
    string_names = ["e", "B", "G", "D", "A", "E"]
    for i, name in enumerate(string_names):
        text_surface = font.render(name + "|", True, BLACK)
        screen.blit(text_surface, (70, start_y + (i * line_spacing) - 20))

    # Draw the tab numbers
    note_spacing = 50
    for string_idx, string_notes in enumerate(current_tab):
        for note_idx, fret in enumerate(string_notes):
            x = 100 + (note_idx * note_spacing)
            y = start_y + (string_idx * line_spacing) - 20
            if fret == -1:
                text_surface = font.render("-", True, BLACK)
            else:
                text_surface = font.render(str(fret), True, BLACK)
            screen.blit(text_surface, (x, y))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit() 