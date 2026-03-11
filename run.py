# run.py 
import sys 
import json 
import argparse 
from pathlib import Path 
 
sys.path.insert(0, str(Path(__file__).parent)) 
 
try: 
    from video_composer import make_short_video 
    print("Video composer imported successfully") 
except Exception as e: 
    print(f"Import error: {e}") 
    sys.exit(1) 
 
def main(): 
    parser = argparse.ArgumentParser() 
    parser.add_argument('--json', required=True) 
    parser.add_argument('--images', type=int, default=4) 
    args = parser.parse_args() 
 
    with open(args.json, 'r', encoding='utf-8') as f: 
        data = json.load(f) 
 
    images = [] 
 
    result = make_short_video( 
        images=images, 
        audio_path=None, 
        english_text=data['details'], 
        headline=data['headline'], 
        hook=data['hook_text'], 
        subscribe_hook=data['subscribe_hook'], 
        output_path=f"output/{data['headline'][:30]}.mp4" 
    ) 
 
    print(f"Video created: {result}") 
 
if __name__ == "__main__": 
    main() 
