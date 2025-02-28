from flask import Flask, request, jsonify, render_template
import pygame
import os

# Initialize Pygame mixer
try:
    pygame.mixer.init()
    print("Pygame mixer initialized successfully")
    print(f"Using audio driver: {pygame.mixer.get_init()}")
except Exception as e:
    print(f"Failed to initialize Pygame mixer: {e}")

app = Flask(__name__)

# Load sounds
sound_dir = './sounds/'  # Using relative path
print(f"Looking for sound files in: {os.path.abspath(sound_dir)}")  # Print absolute path

keys = [
    # Existing notes
    ('A0', 'A0.wav'),
    ('A1', 'A1.wav'),
    ('A2', 'A2.wav'),
    ('A3', 'A3.wav'),
    ('A4', 'A4.wav'),
    ('A5', 'A5.wav'),
    ('A6', 'A6.wav'),
    ('A7', 'A7.wav'),
    ('Ab1', 'Ab1.wav'),
    ('Ab2', 'Ab2.wav'),
    ('Ab3', 'Ab3.wav'),
    ('Ab4', 'Ab4.wav'),
    ('Ab5', 'Ab5.wav'),
    ('Ab6', 'Ab6.wav'),
    ('Ab7', 'Ab7.wav'),
    ('B0', 'B0.wav'),
    ('B1', 'B1.wav'),
    ('B2', 'B2.wav'),
    ('B3', 'B3.wav'),
    # New notes
    ('C0', 'Bb4.wav'),  
    ('C1', 'C1.wav'),   
    ('C2', 'C2.wav'),
    ('C3', 'C3.wav'),
    ('C4', 'C4.wav'),
    ('C5', 'C5.wav'),
    ('C6', 'C6.wav'),
    ('C7', 'C7.wav'),
    ('D0', 'C8.wav'),  #
    ('D1', 'D1.wav'),
    ('D2', 'D2.wav'),
    ('D3', 'D3.wav'),
    ('D4', 'D4.wav'),
    ('D5', 'D5.wav'),
    ('D6', 'D6.wav'),
    ('D7', 'D7.wav'),
    ('E0', 'Db1.wav'),  #
    ('E1', 'E1.wav'),
    ('E2', 'E2.wav'),
    ('E3', 'E3.wav'),
    ('E4', 'E4.wav'),
    ('E5', 'E5.wav'),
    ('E6', 'E6.wav'),
    ('E7', 'E7.wav'),
    ('F0', 'Eb1.wav'),  #
    ('F1', 'F1.wav'),
    ('F2', 'F2.wav'),
    ('F3', 'F3.wav'),
    ('F4', 'F4.wav'),
    ('F5', 'F5.wav'),
    ('F6', 'F6.wav'),
    ('F7', 'F7.wav'),
    ('G0', 'Gb1.wav'),  #
    ('G1', 'G1.wav'),
    ('G2', 'G2.wav'),
    ('G3', 'G3.wav'),
    ('G4', 'G4.wav'),
    ('G5', 'G5.wav'),
    ('G6', 'G6.wav'),
    ('G7', 'G7.wav'),
    ('C#0', 'Gb2.wav'),
    ('D#0', 'Gb3.wav'),
    ('F#0', 'Gb4.wav'),
    ('G#0', 'Gb5.wav'),
    ('D#3', 'Gb6.wav'),
    ('F#3', 'Gb7.wav'),
    ('F#1', 'Ab2.wav'),
    ('G#1', 'Ab3.wav'),
    ('A#1', 'Ab4.wav'),
    ('C#2', 'Ab5.wav'),
    ('D#2', 'Ab6.wav'),
    ('F#2', 'Ab7.wav'),
    ('G#2', 'Bb4.wav'),
    ('A#2', 'Bb5.wav'),
    ('C#3', 'Bb6.wav'),

]

sounds = {}
missing_files = []
for note, file in keys:
    try:
        sound_path = sound_dir + file
        sounds[note] = pygame.mixer.Sound(sound_path)
        print(f"Successfully loaded: {file}")
    except FileNotFoundError:
        missing_files.append(file)
        print(f"Warning: File not found: {sound_path}")
    except Exception as e:
        print(f"Error loading {file}: {str(e)}")

if missing_files:
    print("\nMissing sound files:")
    for file in missing_files:
        print(f"- {file}")

@app.route('/')
def home():
    return render_template('piano.html')  # Serve the piano interface

@app.route('/notes', methods=['GET'])
def get_notes():
    return jsonify([note for note, _ in keys])

@app.route('/play', methods=['POST'])
def play_note():
    note = request.json.get('note')
    if note in sounds:
        sounds[note].play()
        return jsonify({'status': 'playing', 'note': note}), 200
    else:
        return jsonify({'error': 'Note not found'}), 404

@app.route('/stop', methods=['POST'])
def stop_note():
    note = request.json.get('note')
    if note in sounds:
        sounds[note].stop()
        return jsonify({'status': 'stopped', 'note': note}), 200
    else:
        return jsonify({'error': 'Note not found'}), 404

if __name__ == '__main__':
    # For production, disable debug mode
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)