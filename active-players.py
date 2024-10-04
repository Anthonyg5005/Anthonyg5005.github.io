import os
import time
import re
import sys

log_directory = None
player_instances = {}

def get_current_time():
    return time.strftime("%I:%M %p")

def process_log_line(line):
    join_pattern = r"\d{4}\.\d{2}\.\d{2} (\d{2}:\d{2}:\d{2}) Log\s+-\s+\[Behaviour\] OnPlayerJoined\s+(.*)"
    leave_pattern = r"\d{4}\.\d{2}\.\d{2} (\d{2}:\d{2}:\d{2}) Log\s+-\s+\[Behaviour\] OnPlayerLeft\s+(.*)"
    exit_pattern = r"\d{4}\.\d{2}\.\d{2} (\d{2}:\d{2}:\d{2}) Log\s+-\s+\[EOSManager\] PlatformInterface\.ShutDown: Success"
    join_match = re.match(join_pattern, line)
    leave_match = re.match(leave_pattern, line)
    exit_match = re.match(exit_pattern, line)
    
    if join_match:
        timestamp = join_match.group(1)
        player_name = join_match.group(2)
        player_instances[player_name] = timestamp
    elif leave_match:
        timestamp = leave_match.group(1)
        player_name = leave_match.group(2)
        if player_name in player_instances:
            del player_instances[player_name]
    elif exit_match:
        print("VRChat has been closed. Press Enter to exit.")
        input()
        sys.exit()

def read_log_file(log_file_path):
    try:
        with open(log_file_path, "r", encoding="utf-8") as log_file:
            for line in log_file:
                process_log_line(line)
    except FileNotFoundError:
        print("Log file not found.")

def clear_console():
    os.system('cls')

def main():
    global log_directory
    log_directory = os.path.join(os.getenv('AppData'), '..', 'LocalLow', 'VRChat', 'VRChat')
    
    print("Monitoring VRChat player instances. Press Ctrl+C to exit.")
    while True:
        clear_console()
        
        files = os.listdir(log_directory)
        txt_files = [f for f in files if f.endswith('.txt')]
        txt_files.sort(key=lambda x: os.stat(os.path.join(log_directory, x)).st_mtime, reverse=False)
        
        if txt_files:
            log_file_path = os.path.join(log_directory, txt_files[-1])
            read_log_file(log_file_path)
        
        print("Active Player Instances:")
        for player_name, timestamp in player_instances.items():
            formatted_time = time.strftime("%I:%M %p", time.strptime(timestamp, "%H:%M:%S"))
            print(f"{formatted_time} - {player_name}")
        
        print("-" * 30)
        time.sleep(15)

if __name__ == "__main__":
    main()
