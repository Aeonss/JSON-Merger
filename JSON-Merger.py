import json
import os
import sys
from pathlib import Path
from collections import defaultdict

encoding = 'utf-8'
indentNum = 4

def clean(data):
    return json.dumps(data, sort_keys=True, indent=indentNum, separators=(',', ': '))

dir = sys.argv[1]

out = []
files_ignored = []
num_files = 0
num_ignored = 0


for root, subdirs, files in os.walk(os.path.abspath(dir)):
    if (root.startswith('.')): 
        continue
    
    dirname = os.path.basename(root)

    output_file = os.path.join(os.path.join(root, os.pardir), dirname + '-output.json')

    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    for filename in files:

        file_path = os.path.join(root, filename)

        if filename.endswith('.json'):
            print('Appended: ' + filename)

            try:
                with open(file_path, 'r', encoding = encoding) as f:
                    data = f.read()
                    content = json.loads(data)
                    out.append(content)
                    num_files = num_files + 1

            except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                files_ignored.append(filename)
                num_ignored = num_ignored + 1

    clean_content = clean(out)
        
    with open(output_file, 'wb+') as out_file:
        out_file.write(clean_content.encode(encoding))

# Print out statistics

print('\n----------------------------------------')
print('Number of files merged: ' + str(num_files))
print('Number of files ignored: ' + str(num_ignored))

if num_ignored > 0:
    print('\nFaulty Files:')
    for i in range(len(files_ignored)):
        print('\t' + files_ignored[i])

print('----------------------------------------')