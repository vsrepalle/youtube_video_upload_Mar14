import os

LOG_FILE = "last_channel.txt"
CHANNELS = ["trendwave", "spacemind", "wonderfacts"]

def get_next():
    if not os.path.exists(LOG_FILE):
        return CHANNELS[0]
    
    with open(LOG_FILE, "r") as f:
        last = f.read().strip().lower()
    
    try:
        current_index = CHANNELS.index(last)
        next_index = (current_index + 1) % len(CHANNELS)
        return CHANNELS[next_index]
    except ValueError:
        return CHANNELS[0]

def save_last(channel):
    with open(LOG_FILE, "w") as f:
        f.write(channel)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        save_last(sys.argv[1])
    else:
        print(get_next())
