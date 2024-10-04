import os
import time
import re
from datetime import datetime

print("Keep window open for automatic refresh every 30 seconds. 30 second wait is to prevent high cpu usage by not having it search through all vrc log files in the past 24 hours multiple times a second")

while True:
  appdata_dir = os.getenv('AppData')
  vrchat_dir = os.path.join(appdata_dir, '..', 'LocalLow', 'VRChat', 'VRChat')

  files = os.listdir(vrchat_dir)
  txt_files = [f for f in files if f.endswith('.txt')]
  txt_files.sort(key=lambda x: os.stat(os.path.join(vrchat_dir, x)).st_mtime, reverse=False)

  output_file = open('instance history.html', 'w', encoding='utf-8')

  output_file.write('<html>\n')
  output_file.write('<head>\n')
  output_file.write('<title>Instance History</title>\n')
  output_file.write('<meta http-equiv="refresh" content="5">\n')
  output_file.write('<style>\n')
  output_file.write('h1 {text-align: center; font-family: Arial; color: #36d7ff;}\n')
  output_file.write('body {font-family: Arial; background-color: #1f1f1f;}\n')
  output_file.write('table {border-collapse: collapse; width: 100%;}\n')
  output_file.write('td, th {border: 2px solid rgba(0, 0, 0); border-top: 0px solid; padding: 4px; color: #bebebe; background-color: #383838;}\n')
  output_file.write('td {padding: 0px; border-top: 4px solid rgba(0, 0, 0);}\n')
  output_file.write('td a {color: #df9d52; text-decoration: underline;}\n')
  output_file.write('th {text-align: center; background-color: #7fe4fd; color: rgb(0, 0, 0);\n')
  output_file.write('tr {background-color: #383838;}\n')
  output_file.write('</style>\n')
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
    with open(os.path.join(vrchat_dir, txt_file), 'r', encoding='utf-8') as f:
      log_contents = f.read()

    lines = log_contents.split('\n')

    counter = 0
    total_lines = len(lines)
    for line in lines:
      if '[Behaviour] Joining' in line:
        counter += 1
        output_file.write('<tr>\n')

        # Convert the timestamp to a more readable format
        timestamp = datetime.strptime(line[0:19], "%Y.%m.%d %H:%M:%S")
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        output_file.write('<td>' + formatted_timestamp + '</td>\n')

        output_string = line[line.index('[Behaviour] Joining'):].replace('[Behaviour] Joining', '').replace('or Creating Room:', '')

        world_id_match = re.search(r'wrld_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', output_string)
        world_id = world_id_match.group() if world_id_match else ''
        instance_id = output_string[output_string.index(':') + 1:] if ':' in output_string else ''

        link = f"https://vrchat.com/home/launch?worldId={world_id}&instanceId={instance_id}"

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

  output_file.close()

  time.sleep(30)
