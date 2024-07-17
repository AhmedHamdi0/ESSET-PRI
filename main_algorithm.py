from sniffing import Sniffing
from replay_attack import ReplayAttack
from fuzzing import Fuzzing
from intercept import Intercept
import json
from programming import Programming


with open("/home/esset/FTP/files/config/config.json", "r") as file:
    config = json.load(file)
    operation = config.get("operation")
    sniffing_time = config.get("sniffing_time")
    svf_file = config.get("svf_file")
    programming = config.get("programming")


if programming:
    prog = Programming(svf_file)
    prog.run()

if operation == "Sniffing":
    sniff = Sniffing()
    sniff.run(sniffing_time)

elif operation == "Replay Attack":
    replay_attack = ReplayAttack()
    replay_attack.run()

elif operation in ["Conditional Bypass", "Stream Finder"]:
    intercept = Intercept()
    intercept.run()

elif operation == "Fuzzing":
    fuzz = Fuzzing()
    fuzz.run()

else:
    pass
