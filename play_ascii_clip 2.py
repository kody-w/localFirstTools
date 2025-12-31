#!/usr/bin/env python3
import json
import sys
import time
import os

def clear_screen():
    # ANSI escape code to clear screen and move cursor to top-left
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()

def play_clip(filename, fps=30):
    try:
        with open(filename, 'r') as f:
            frames = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: File '{filename}' is not a valid JSON recording.")
        return

    delay = 1.0 / fps
    
    try:
        # Hide cursor
        sys.stdout.write('\033[?25l')
        
        for frame in frames:
            # Move cursor to top-left instead of full clear to reduce flicker
            sys.stdout.write('\033[H')
            sys.stdout.write(frame)
            sys.stdout.flush()
            time.sleep(delay)
            
    except KeyboardInterrupt:
        pass
    finally:
        # Show cursor again
        sys.stdout.write('\033[?25h')
        print("\nDone.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 play_ascii_clip.py <filename.json> [fps]")
        print("Example: python3 play_ascii_clip.py ascii-clip-123456.json")
        sys.exit(1)
        
    filename = sys.argv[1]
    fps = 30
    if len(sys.argv) > 2:
        try:
            fps = int(sys.argv[2])
        except ValueError:
            pass
            
    play_clip(filename, fps)
