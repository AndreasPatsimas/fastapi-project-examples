from datetime import datetime
import os

cwd = os.getcwd()

with open(os.path.join(cwd, "test.txt"), "a") as f:
    f.write("Accessed test2.py on " + str(datetime.now()) + "\n")
