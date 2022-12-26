import os
import click

mypath = "indexes_cdx/"
extension = "cdxj"

data = {}

for subdir, dirs, files in os.walk(mypath):
    if files:
        with click.progressbar(length=len(files), show_pos=True) as progress_bar:
            for file in files:
                progress_bar.update(1)
                if file.endswith(extension):
                    findFileExtension = True
                    file_name = os.path.join(subdir, file)
                    with open(file_name, 'r') as stream:
                        for line in stream:
                            list_line = line.split(" ")
                            try:
                                mime = list_line[list_line.index("\"mime\":")+1].replace("\",", "").replace("\"", "")
                            except:
                                mime = "NULL"
                            if mime not in data:
                                data[mime] = 1
                            else:
                                data[mime] += 1

for key, value in sorted(data.items(), key=lambda x: x[1], reverse=True): 
    print("{} : {}".format(key, value))