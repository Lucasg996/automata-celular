from flask import Flask, send_file, render_template, jsonify
import pygame
import numpy as np
import io

app = Flask(__name__)

# Configuración de la pantalla
width, height = 400, 400
cell_size = 10
space_size = 15
grid_width = (width - space_size) // (cell_size + space_size)
grid_height = (height - space_size) // (cell_size + space_size)
update_interval = 100

# Inicializa Pygame
pygame.init()
pygame.mixer.init()  # Inicializa el módulo de sonido

# Variables globales para sonido
sound_volume = 0.1
sound_muted = False

# Función para generar un sonido
def play_note(frequency, duration=0.5, sample_rate=44100):
    if sound_muted:
        return
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(frequency * t * 2 * np.pi)
    audio = np.int16(wave * 32767 * sound_volume)
    sound = pygame.mixer.Sound(audio.tobytes())
    sound.play()

def initialize_grid():
    return np.random.randint(0, 2, (grid_height, grid_width), dtype=int)

def update_grid(grid):
    new_grid = np.copy(grid)
    for y in range(grid_height):
        for x in range(grid_width):
            if np.random.rand() < 0.1:
                new_grid[y, x] = 1 - grid[y, x]
    return new_grid

def generate_color_pattern(grid):
    color_pattern = np.ones((height, width, 3), dtype=np.uint8) * 0
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y, x] == 1:
                color = (255, 255, 255)
                y_start = y * (cell_size + space_size)
                x_start = x * (cell_size + space_size)
                color_pattern[y_start:y_start + cell_size, x_start:x_start + cell_size] = color
                
                frequency = 200 + (x * 5)  
                play_note(frequency)
            else:
                frequency = 100 + (x * 3)
                play_note(frequency)
    return color_pattern

# Inicializa la cuadrícula
grid = initialize_grid()

@app.route('/image')
def image():
    global grid
    grid = update_grid(grid)
    color_pattern = generate_color_pattern(grid)
    
    surface = pygame.surfarray.make_surface(np.transpose(color_pattern, (1, 0, 2)))
    
    img_bytes = io.BytesIO()
    pygame.image.save(surface, img_bytes, 'PNG')
    img_bytes.seek(0)
    
    return send_file(img_bytes, mimetype='image/png')

@app.route('/set_volume/<float:volume>')
def set_volume(volume):
    global sound_volume
    sound_volume = volume
    return jsonify(success=True)

@app.route('/mute')
def mute():
    global sound_muted
    sound_muted = not sound_muted
    return jsonify(muted=sound_muted)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
