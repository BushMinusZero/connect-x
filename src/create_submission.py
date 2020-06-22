import inspect
import os
from agents import agent_random


def write_agent_to_file(function, file):
    with open(file, "a" if os.path.exists(file) else "w") as f:
        f.write(inspect.getsource(function))
        print(function, "written to", file)


write_agent_to_file(agent_random, "submission.py")
