import os
import subprocess
import argparse

def extract_english_subtitles(video_file):
    # Check if the video file exists
    if not os.path.exists(video_file):
        print("Error: Video file not found")
        return

    # Define a dummy output file (it won't actually be created)
    # dummy_output = os.devnull  # Linux/Unix
    dummy_output = 'NUL'  # Windows

    # Execute FFmpeg command to get subtitle information
    try:
        result = subprocess.run(['ffmpeg', '-i', video_file, '-f', 'null', dummy_output], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error 1:", e)
        return

    # Parse FFmpeg output to find English subtitle track
    subtitle_tracks = []
    for line in result.stderr.split('\n'):
        if 'Subtitle' in line:
            parts = line.split(',')
            for part in parts:
                if 'eng' in part.lower():
                    subtitle_tracks.append(int(parts[0].strip().split()[1][:-1]))

    if not subtitle_tracks:
        print("No English subtitle track found")
        return

    # Extract subtitles from the first English subtitle track found
    subtitle_track = subtitle_tracks[0]
    filename, _ = os.path.splitext(video_file)
    subtitle_file = f"{filename}_english.srt"

    # Execute FFmpeg command to extract English subtitles
    try:
        subprocess.run(['ffmpeg', '-i', video_file, '-map', f'0:s:{subtitle_track}', subtitle_file], check=True)
        print("English subtitles extracted successfully")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract English subtitles from a video file")
    parser.add_argument("video_file", help="Path to the video file")
    args = parser.parse_args()

    extract_english_subtitles(args.video_file)
