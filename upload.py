import os

file = open('/home/cris-edwards/Desktop/history.txt', 'r')

new_title = file.readline()
new_title = new_title.replace(":", "").replace(" ", "_").replace("/", "_").strip()+".txt"
command = f'cp history.txt {new_title}'
os.system(command)
command = f'git add {new_title}'
os.system(command)
os.system('git commit -m "comment"')
os.system('git push')
os.remove(new_title)
