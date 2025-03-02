from packages.environment.cameras import TPSCamera, Camera

import glfw

class CameraManager:

    TPS_CAMERA = "CAMERA-MANAGER-TPS-CAMERA"

    def __init__(self):
        self._camera: Camera.Camera = None
        self._cameras = {}
        self._window = None

    def set_camera(self, camera_name):
        self._camera = self._cameras[camera_name]
        print(type(self._window))
        # glfw.set_scroll_callback(self._window, self._camera.on_scroll)

    def _create_tps_camera(self, name, pos, entity):
        new_camera = TPSCamera.TPSCamera(name, pos, entity)
        self._cameras[name] = new_camera
        return new_camera

    def create_camera(self, camera_type, name, pos, entity=None):
        if camera_type == self.TPS_CAMERA:
            return self._create_tps_camera(name, pos, entity)

    def use_window(self, window):
        print("using window")
        self._window = window

    @property
    def camera(self):
        return self._camera

