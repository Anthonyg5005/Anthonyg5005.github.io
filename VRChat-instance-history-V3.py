import os
import time
import re

# ALL CODE WRITTEN USING chat.openai.com
# I am not good at coding all I can really do is just look at code and modify it

while True:
  # Get the path to the VRChat directory
  appdata_dir = os.getenv('AppData')
  vrchat_dir = os.path.join(appdata_dir, '..', 'LocalLow', 'VRChat', 'VRChat')

  # Get a list of all the files in the VRChat directory
  files = os.listdir(vrchat_dir)

  # Filter the list to include only .txt files
  txt_files = [f for f in files if f.endswith('.txt')]

  # Sort the list of .txt files by last modified date (oldest first)
  txt_files.sort(key=lambda x: os.stat(os.path.join(vrchat_dir, x)).st_mtime, reverse=False)

  # Create a new file to write the output to
  output_file = open('instance history.html', 'w', encoding='utf-8')

  output_file.write('<html>\n')
  output_file.write('<head>\n')
  output_file.write('<title>Instance History</title>\n')
  output_file.write('<meta http-equiv="refresh" content="15">\n')
  output_file.write('</head>\n')
  output_file.write('<body>\n')
  output_file.write('<h1>Instance History</h1>\n')
  output_file.write('<table>\n')
  output_file.write('<tr>\n')
  output_file.write('<th>Time</th>\n')
  output_file.write('<th>Instance</th>\n')
  output_file.write('</tr>\n')

  line_counter = 0
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
        output_file.write('<tr>\n')
        output_file.write('<td>' + line[1:17] + '</td>\n')

        output_string = line[line.index('[Behaviour] Joining'):].replace('[Behaviour] Joining', '').replace('or Creating Room:', '')

        # Extract the world ID and instance ID from the output string
        world_id_match = re.search(r'wrld_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', output_string)
        world_id = world_id_match.group() if world_id_match else ''
        instance_id = output_string[output_string.index(':') + 1:] if ':' in output_string else ''

        # Construct the link
        link = f"https://vrchat.com/home/launch?worldId={world_id}&instanceId={instance_id}"

        # Create the HTML link
        html_link = f"<a href='{link}'>{output_string}</a>"

        if 'wrld_' in output_string:
          output_file.write('<td>' + html_link + '</td>\n')
        else:
          output_file.write('<td>' + output_string + '</td>\n')
        output_file.write('</tr>\n')
        line_counter += 1
        if line_counter % 2 == 0 and line_counter < total_lines:
          output_file.write('<tr><td></td><td></td></tr>\n')

  output_file.write('</table>\n')
  output_file.write('</body>\n')
  output_file.write('</html>\n')

  # Close the output file
  output_file.close()

  time.sleep(30)
