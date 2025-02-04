import engine

def start():
    print("hello world")

engine = engine.Engine()
engine.set_on_load(start)
engine.run()