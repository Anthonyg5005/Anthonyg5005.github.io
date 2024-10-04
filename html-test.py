import os
import time

while True:
  # Get the path to the VRChat directory
  appdata_dir = os.getenv('AppData')
  vrchat_dir = os.path.join(appdata_dir, '..', 'LocalLow', 'VRChat', 'VRChat')

  # Get a list of all the files in the VRChat directory
  files = os.listdir(vrchat_dir)

  # Filter the list to include only .txt files
  txt_files = [f for f in files if f.endswith('.txt')]

  # Sort the list of .txt files by last modified date (newest first)
  txt_files.sort(key=lambda x: os.stat(os.path.join(vrchat_dir, x)).st_mtime, reverse=True)

  # Create a new file to write the output to
  output_file = open('instance history.html', 'w', encoding='utf-8')

  for txt_file in txt_files:
    # Open the .txt file with the specified character encoding
    with open(os.path.join(vrchat_dir, txt_file), 'r', encoding='utf-8') as f:
      log_contents = f.read()

    # Split the log contents into a list of lines
    lines = log_contents.split('\n')

    counter = 0
    total_lines = len(lines)
    for line in lines:
      if '[Behaviour] Joining' in line:
        counter += 1
        output_file.write(line + '\n')
        if counter % 2 == 0 and counter < total_lines:
          output_file.write('\n')

  # Close the output file
  output_file.close()

  # Open the output file using the default text editor in Windows
  # subprocess.run(['start', 'instance history'], shell=True)

  time.sleep(30)
