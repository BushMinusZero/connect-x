from kaggle_environments import make, evaluate
from tutorial1 import agent1, agent2
from tutorial2 import agent3
from tutorial3 import agent

# Create the game environment
# Set debug=True to see the errors if your agent refuses to run
env = make("connectx", debug=True)

# List of available default agents
print(list(env.agents))

# Two random agents play one game round
env.run([agent, agent])

# Show the game
rendered = env.render(mode="html")

with open("env.html", "w") as f:
    f.write(rendered)
