import engine

def start(eng: engine.Engine):
    eng.current_scene.spawn_entity("models\\cube")


engine = engine.Engine()
engine.on_loaded = start
engine.create_scene("Main_scene")
engine.use_scene("Main_scene")
engine.add_script_folder("models")

engine.create_entity_template("player", "packages/other/entities/models/cube.json")
# engine.create_entity_template("player", "packages/other/entities/models/player.json")
player = engine.current_scene.spawn_entity("player")

engine.current_scene.create_camera(engine.current_scene.TPS_CAMERA, "cam1", [0, 0, 0], player)
engine.current_scene.set_camera("cam1")
engine.run_logic_only()