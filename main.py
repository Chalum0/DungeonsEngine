import engine

def start():
    print("hello world")

engine = engine.Engine()
# engine.set_on_load(start)
engine.create_scene("Main_scene")
engine.use_scene("Main_scene")
engine.current_scene.create_entity_template("player", "packages/other/entities/models/cube.json")
player = engine.current_scene.spawn_entity("player")

engine.current_scene.create_camera(engine.current_scene.TPS_CAMERA, "cam1", [0, 0, 0], player)
engine.current_scene.set_camera("cam1")
engine.run()