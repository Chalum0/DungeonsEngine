import time

class Clock:
    def __init__(self):
        self.starting_time = time.time()
        self.timer = 0.0

        self.dt = 0
        self.fps = 0
        self.frame = 0

        self.second = 0

        self.display_fps = False

        self._frame_count = 0
        self._last_frame_time = 0
        self._last_fps_time = 0

    def get_frame(self):
        return self.frame * 10000

    def tick(self):
        current_time = time.perf_counter()
        if self._last_frame_time == 0:
            self._last_frame_time = current_time

        # Calculate delta time
        self.dt = current_time - self._last_frame_time
        self._last_frame_time = current_time

        # Update frame count
        self._frame_count += 1
        self.frame += .0001

        # Update FPS every second
        if current_time - self._last_fps_time >= 1.0:
            self.fps = self._frame_count
            self._frame_count = 0
            self._last_fps_time = current_time
            self.second += 1
            if self.display_fps:
                print(f"FPS: {self.fps}")