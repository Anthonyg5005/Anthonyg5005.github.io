import os

# Get the path to the VRChat directory
appdata_dir = os.getenv('AppData')
vrchat_dir = os.path.join(appdata_dir, '..', 'LocalLow', 'VRChat', 'VRChat')
files = os.listdir(vrchat_dir)
txt_files = [f for f in files if f.endswith('.txt')]
txt_files.sort(key=lambda x: os.stat(os.path.join(vrchat_dir, x)).st_mtime, reverse=False)
for txt_file in txt_files:
  with open(os.path.join(vrchat_dir, txt_file), 'r', encoding='utf-8') as f:
    log_contents = f.read()
  lines = log_contents.split('\n')
  counter = 0
  total_lines = len(lines)
  for line in lines:
    if '[Behaviour] Joining' in line:
      counter += 1
      print(line)
      if counter % 2 == 0 and counter < total_lines:
        print('\n')
