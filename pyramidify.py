import numpy as np
import plotly.graph_objects as go

class CameraPlotter:

    def __init__(self, transforms, camera_size=0.4):
        self.ca_x = transforms['camera_angle_x']
        self.ca_y = transforms['camera_angle_y']
        self.camera_size = float(camera_size)
        self.points = [[ 0,  1,  1, -1, -1], # pyramid verticies
                       [ 0,  1, -1, -1,  1],
                       [ 0,  1,  1,  1,  1]]
        self.lines = [[1, 2], [2, 3], [3, 4], [4, 1], # pyramid lines
                      [0, 1], [0, 2], [0, 3], [0, 4]]
        self.camera_list = []

    def camera_to_world(self, M_ext):
        R = M_ext[:3, :3] # rotation matrix
        t = M_ext[:3, 3] # translation vector
        camera = np.array(self.points) * self.camera_size
        camera[0, :] *= np.tan(self.ca_x/2)
        camera[1, :] *= np.tan(self.ca_y/2)
        camera = -((R @ camera).T - t).T
        return camera

    def add_camera(self, M_ext, color, name):
        camera = self.camera_to_world(M_ext)
        self.camera_list.append((camera, color, name))

    def update_camera(self, M_ext, color, name):
        camera = self.camera_to_world(M_ext)
        del self.camera_list[-1]
        self.camera_list.append((camera, color, name))

    def plot_cameras(self):
        fig = go.Figure()
        for n, (camera, color, name) in enumerate(self.camera_list):
            for i, j in self.lines:
                x, y, z = [[axis[i], axis[j]] for axis in camera]
                trace = go.Scatter3d(x=x, y=y, z=z, mode='lines', line_width=2, line_color=color, name=name)
                fig.add_trace(trace)
            x, y, z = camera[:, 1:]
            mesh = go.Mesh3d(x=x, y=y, z=z, opacity=0.5, color=color, name=name)
            fig.add_trace(mesh)
        fig.update_layout(showlegend=False)
        fig.show()

class CameraMover:
    def __init__(self):
        self.M_ext = M_ext = np.array([[1, 0, 0, 0],
                                       [0, 1, 0, 0],
                                       [0, 0, 1, 0],
                                       [0, 0, 0, 1]], dtype=float)

    def step_x(self, size):
        self.M_ext[0, 3] += size

    def step_y(self, size):
        self.M_ext[1, 3] += size

    def step_z(self, size):
        self.M_ext[2, 3] += size

    def rotate_x(self, angle):
        angle = np.radians(angle)
        R_theta = np.array([[np.cos(angle), 0, -np.sin(angle), 0],
                            [0, 1, 0, 0],
                            [np.sin(angle), 0, np.cos(angle), 0],
                            [0, 0, 0, 1]], dtype=float)
        self.M_ext = R_theta @ self.M_ext

    def rotate_y(self, angle):
        angle = np.radians(angle)
        R_phi = np.array([[1, 0, 0, 0],
                          [0, np.cos(angle), -np.sin(angle), 0],
                          [0, np.sin(angle), np.cos(angle), 0],
                          [0, 0, 0, 1]], dtype=float)
        self.M_ext = R_phi @ self.M_ext

    def rotate_z(self, angle):
        angle = np.radians(angle)
        R_psi = np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                          [np.sin(angle), np.cos(angle), 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]], dtype=float)
        self.M_ext = R_psi @ self.M_ext
