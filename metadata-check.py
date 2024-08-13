import exifread
import os
import json
import subprocess
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image_path):
    exif_data = {}
    with open(image_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)
        for tag, value in tags.items():
            tag_name = TAGS.get(tag, tag)
            exif_data[tag_name] = str(value)
    
    return exif_data

def get_ffmpeg_metadata(video_path):
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_path
    ]
    ffprobe_output = subprocess.check_output(cmd).decode('utf-8')
    ffprobe_data = json.loads(ffprobe_output)
    
    return ffprobe_data

def main():
    file_path = input("Enter the filepath for an image or video: ").strip()

    if not os.path.exists(file_path):
        print("[!] File does not exist.")
        return

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in ['.jpg', '.jpeg', '.png']:
        print("[*] Extracting EXIF data from image...")
        exif_data = get_exif_data(file_path)

        if exif_data:
            print("[*] EXIF metadata:")
            for key, value in exif_data.items():
                print(f"\t{key}: {value}")
        else:
            print("[!] No EXIF metadata found in this image.")
    elif file_extension in ['.mp4', '.mkv', '.avi', '.mov']:
        print("[*] Extracting metadata from video...")
        metadata = get_ffmpeg_metadata(file_path)

        if metadata:
            print("[*] Video metadata:")
            print(json.dumps(metadata, indent=4))
        else:
            print("[!] No metadata found in this video.")
    else:
        print("[!] Unsupported file format.")

if __name__ == "__main__":
    main()
