import numpy as np
import os
import json

# 读取的文件
# image_path = "data/0" # COLMAP原始的结果
image_path = "data/1"  # COLMAP对齐前20帧坐标真值的结果


# 四元数到旋转矩阵
def qvec2rotmat(qvec):
    return np.array([
        [
            1 - 2 * qvec[2] ** 2 - 2 * qvec[3] ** 2,
            2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
            2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]
        ], [
            2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
            1 - 2 * qvec[1] ** 2 - 2 * qvec[3] ** 2,
            2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]
        ], [
            2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
            2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
            1 - 2 * qvec[1] ** 2 - 2 * qvec[2] ** 2
        ]
    ])


# 用colmap2nerf的方法读取，但不改变c2w
with open(os.path.join(image_path, "images.txt"), "r") as f:
    i = 0

    bottom = np.array([0.0, 0.0, 0.0, 1.0]).reshape([1, 4])

    frames = []

    for line in f:
        line = line.strip()

        if line[0] == "#":
            continue

        i = i + 1

        if i % 2 == 1:
            elems = line.split(" ")  # 1-4 is quat, 5-7 is trans, 9ff is filename (9, if filename contains no spaces)
            name = '_'.join(elems[9:])

            qvec = np.array(tuple(map(float, elems[1:5])))
            tvec = np.array(tuple(map(float, elems[5:8])))
            R = qvec2rotmat(-qvec)
            t = tvec.reshape([3, 1])
            m = np.concatenate([np.concatenate([R, t], 1), bottom], 0)
            c2w = np.linalg.inv(m)

            frame = {
                "idx": int(name.split(".")[0].split("C")[1]),
                "transform_matrix": c2w.tolist()
            }

            frames.append(frame)

# 按照id从小到大排序
frames = sorted(frames, key=lambda e: e.__getitem__('idx'))

# 保存位姿到文件中
json_file = open("colmap_pose.json", mode='w')
json.dump({"frames": frames}, json_file, indent=4)

# 提取XYZ坐标
frames_XYZ = []
for frame in frames:
    # 保存到新的list中
    frames_XYZ.append(
        {
            "idx": frame["idx"],
            "xyz": [x[-1] for x in frame["transform_matrix"]][:-1]
        }
    )

# 保存XYZ坐标到文件中
json_file_XYZ = open("colmap_xyz.json", mode='w')
json.dump({"frames": frames_XYZ}, json_file_XYZ, indent=4)
