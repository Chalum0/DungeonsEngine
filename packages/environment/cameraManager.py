class CameraManager:
    def __init__(self):
        self._camera = None
        self._cameras = []

    def _set_camera(self, camera):
        self._camera = camera

    def create_camera(self, name_camera, pos_camera, type_camera):
        
