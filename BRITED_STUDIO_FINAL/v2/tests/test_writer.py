from legacy.agents.leveria_agent import search_leveria
from legacy.agents.angle_agent import choose_angle
from legacy.agents.writer_agent import write_script

subject = "assurance-vie"

knowledge = search_leveria(subject)
angle = choose_angle(subject, knowledge)
script = write_script(subject, knowledge, angle)

print(script)

