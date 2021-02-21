from engine import GameEngine
import platform

if platform.system() == "Darwin":
    window_size = "MEDIUM"
else:
    window_size = "LARGE"
my_engine = GameEngine()
my_engine.run()