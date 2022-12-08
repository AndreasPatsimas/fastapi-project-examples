from datetime import datetime
import os

cwd = os.getcwd()
print("teers")
with open(os.path.join(cwd, "test.txt"), "a") as f:
    f.write("Accessed test1.py on " + str(datetime.now()) + "\n")
