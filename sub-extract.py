import os
import subprocess
import argparse

def extract_english_subtitles(video_file):
    # Check if the video file exists
    if not os.path.exists(video_file):
        print("Error: Video file not found")
        return

    # Extract eng subtitle using ffprobe
    command = [
        'ffprobe',
        '-loglevel', 'error',
        '-select_streams', 's',
        '-show_entries', 'stream=index:stream_tags=language',
        '-of', 'csv=p=0',
        f'{video_file}'
        ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error: ", e)
        return

    # Parse ffprobe output to find English subtitle track
    subtitle_tracks = []

    # storing the first index no matter the language
    for index, line in enumerate(result.stdout.split('\n')):
        if index == 0:
            first_sub_track_offset = line.split(',')[0]
            print(f'Setting the offset: {first_sub_track_offset}')
        if 'eng' in line:
            print(f'Found english sub track at index {line.split(",")[0]}')

            # removing the offset in order to get the true entry
            entry = int(line.split(",")[0]) - int(first_sub_track_offset)
            subtitle_tracks.append(entry)

    if not subtitle_tracks:
        print("No English subtitle track found")
        return

    # Extract subtitles from the first English subtitle track found
    subtitle_track = subtitle_tracks[0]
    filename, _ = os.path.splitext(video_file)
    subtitle_file = f"{filename}.srt"

    # Execute FFmpeg command to extract English subtitles
    command = [
        'ffmpeg', '-i', video_file,
        '-vn', '-an',
        '-map', f'0:s:{subtitle_track}',
        subtitle_file]

    try:
        subprocess.run(['ffmpeg', '-i', video_file, '-map', f'0:s:{subtitle_track}', subtitle_file], check=True)
        print("English subtitles extracted successfully")
    except subprocess.CalledProcessError as e:
        print(f'Error on extracting subtitle: ', e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract English subtitles from a video file")
    parser.add_argument("video_file", help="Path to the video file")
    args = parser.parse_args()

    extract_english_subtitles(args.video_file)
