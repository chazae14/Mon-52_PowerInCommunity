from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Load songs data
import json
with open("songs_database.json", encoding="utf8") as f:
    songs = json.load(f)

# Variables to track the current state
current_song = None
is_playing = False
speed = 1.0

@app.route('/')
def home():
    return render_template("index.html", songs=songs, current_song=current_song, is_playing=is_playing, speed=speed)

@app.route('/play', methods=['POST'])
def play():
    global current_song, is_playing
    song_name = request.json.get('song')
    
    # Find the song in the database
    song = next((s for s in songs if s["song_name"] == song_name), None)
    
    if song:
        current_song = song
        is_playing = True
        return jsonify({"status": "playing", "song_file": song["file"]})
    return jsonify({"status": "error", "message": "Song not found"}), 404

@app.route('/pause', methods=['POST'])
def pause():
    global is_playing
    is_playing = False
    return jsonify({"status": "paused"})

@app.route('/speed', methods=['POST'])
def change_speed():
    global speed
    action = request.json.get('action')
    if action == "up":
        speed += 0.2
    elif action == "down":
        speed = max(0.5, speed - 0.2)
    return jsonify({"status": "speed_changed", "speed": speed})

if __name__ == "__main__":
    app.run(debug=True)
