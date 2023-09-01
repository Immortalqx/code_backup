import open3d as o3d
import open3d.visualization.gui as gui
import numpy as np


# TODO
#  - **模式一：有场景点云**。原始点云与场景点云作差，得到目标点云。
#  - **模式二：无场景点云**。根据坐标对原始点云进行直通滤波，得到目标点云。
#  - **User-Friendly**
#    - 支持滑动条修改xyz坐标轴阈值；
#    - 支持实时显示滤波后的点云；
#    - 支持上下方向键切换上下帧点云；
#    - 支持回车键保存当前点云。

def filter_points(point_cloud):
    """
    输入open3d读入的pcd点云数据point_cloud，输出指定方框内的点云point_cloud_filtered
    """
    points_array = np.asarray(point_cloud.points)

    x = points_array[:, 0]
    y = points_array[:, 1]
    z = points_array[:, 2]

    field_x1 = x < LIMITS["x_up"]
    field_x2 = x > LIMITS["x_low"]
    field_y1 = y < LIMITS["y_up"]
    field_y2 = y > LIMITS["y_low"]
    field_z1 = z < LIMITS["z_up"]
    field_z2 = z > LIMITS["z_low"]

    field = np.logical_and(field_x1, field_x2)
    field = np.logical_and(field, np.logical_and(field_y1, field_y2))
    field = np.logical_and(field, np.logical_and(field_z1, field_z2))
    points_array = points_array[field, :]

    point_cloud_filtered = o3d.geometry.PointCloud()
    point_cloud_filtered.points = o3d.utility.Vector3dVector(points_array)

    return point_cloud_filtered


# ======================== 创建坐标轴阈值 ========================
# FIXME:1米是不是太大了？特别是Z轴，是不是应该好好的处理一下？
LIMITS = {
    "x_up": 100,
    "x_low": -100,
    "y_up": 100,
    "y_low": -100,
    "z_up": 10,
    "z_low": -10
}

# ======================== 创建滑动条控件 ========================
CTRLS = {
    "x_up": gui.Slider(gui.Slider.Type(0)),
    "x_low": gui.Slider(gui.Slider.Type(0)),
    "y_up": gui.Slider(gui.Slider.Type(0)),
    "y_low": gui.Slider(gui.Slider.Type(0)),
    "z_up": gui.Slider(gui.Slider.Type(0)),
    "z_low": gui.Slider(gui.Slider.Type(0))
}

# ======================== 添加取值范围 ========================
CTRLS["x_up"].set_limits(0, 100)
CTRLS["x_low"].set_limits(-100, 0)
CTRLS["y_up"].set_limits(0, 100)
CTRLS["y_low"].set_limits(-100, 0)
CTRLS["z_up"].set_limits(0, 10)
CTRLS["z_low"].set_limits(-10, 0)


# ======================== 设置回调函数 ========================
def call_x_up(val):
    LIMITS["x_up"] = val


def call_x_low(val):
    LIMITS["x_low"] = val


def call_y_up(val):
    LIMITS["y_up"] = val


def call_y_low(val):
    LIMITS["y_low"] = val


def call_z_up(val):
    LIMITS["z_up"] = val


def call_z_low(val):
    LIMITS["z_low"] = val


CTRLS["x_up"].set_on_value_changed(call_x_up)
CTRLS["x_low"].set_on_value_changed(call_x_low)
CTRLS["y_up"].set_on_value_changed(call_y_up)
CTRLS["y_low"].set_on_value_changed(call_y_low)
CTRLS["z_up"].set_on_value_changed(call_z_up)
CTRLS["z_low"].set_on_value_changed(call_z_low)

if __name__ == "__main__":
    point = o3d.io.read_point_cloud("data/01.pcd")
    # # o3d.visualization.draw_geometries([point])
    o3d.visualization.draw_geometries([filter_points(point)])
    # app = gui.Application.instance
    # app.initialize()
    # win = app.create_window("Open3d Test", 500, 150)
    # vert = gui.Vert(0, gui.Margins(2, 2, 2, 2))
    # win.add_child(vert)  # 将布局加载到窗口
    # for key in CTRLS:
    #     vert.add_child(CTRLS[key])
    #
    # app.run()
