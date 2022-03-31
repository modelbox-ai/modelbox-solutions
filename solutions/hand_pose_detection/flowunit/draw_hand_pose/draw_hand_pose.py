#
# Copyright 2021 The Modelbox Project Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import _flowunit as modelbox
import numpy as np
import cv2

class DrawHandPose(modelbox.FlowUnit):
    def __init__(self):
        super().__init__()

    def open(self, config):
        return modelbox.Status.StatusCode.STATUS_SUCCESS

    def process(self, data_context):
        in_image_bufferlist = data_context.input("in_hand_image")
        in_pose_bufferlist = data_context.input("in_pose")
        out_data_buffer_list = data_context.output("out_data")

        for image_buffer, hand_pose_buffer in zip(in_image_bufferlist, in_pose_bufferlist):
            width = image_buffer.get("width")
            height = image_buffer.get("height")
            channel = image_buffer.get("channel")
            out_img = np.array(image_buffer.as_object(), dtype=np.uint8, copy=False)
            out_img = out_img.reshape(height, width, channel)
            out_img = cv2.cvtColor(out_img, cv2.COLOR_RGB2BGR)

            bboxes = image_buffer.get("bboxes")
            bboxes = np.array(bboxes).reshape(-1, 4)
            pose_data = np.array(hand_pose_buffer.as_object(), copy=False).reshape((-1, 21, 2))
            rel_poses = []
            for box, pose in zip(bboxes, pose_data):
                rel_pose = self.draw_hand_pose(out_img, box, pose)
                rel_poses.append(rel_pose)

            add_buffer = modelbox.Buffer(self.get_bind_device(), out_img)
            add_buffer.copy_meta(image_buffer)
            add_buffer.set("pix_fmt", "bgr")
            rel_poses = np.delete(rel_poses, -1, axis=1).astype(int)
            add_buffer.set("hand_pose", rel_poses.flatten().tolist())
            out_data_buffer_list.push_back(add_buffer)

        return modelbox.Status.StatusCode.STATUS_SUCCESS

    def draw_hand_pose(self, img_draw, bbox, in_box_pose):
        h, w, _ = img_draw.shape
        x1, y1, x2, y2 = bbox
        x1 = max(0, int(x1))
        y1 = max(0, int(y1))
        x2 = min(int(x2), w)
        y2 = min(int(y2), h)
        cv2.rectangle(img_draw, (x1, y1), (x2, y2), (0, 0, 255), 2)

        box_w = int(x2 - x1)
        box_h = int(y2 - y1)
        rel_pose = in_box_pose
        rel_pose[:, 0] = x1 + in_box_pose[:, 0] * box_w
        rel_pose[:, 1] = y1 + in_box_pose[:, 1] * box_h

        colors = [(0, 215, 255), (255, 115, 55), (5, 255, 255), (25, 15, 255), (255, 15, 55)]
        for ix in range(5):
            cv2.line(img_draw, (int(rel_pose[0][0]), int(rel_pose[0][1])),
                     (int(rel_pose[ix * 4 + 1][0]), int(rel_pose[ix * 4 + 1][1])), colors[ix], 2)
            for iy in range(3):
                cv2.line(img_draw, (int(rel_pose[ix * 4 + iy + 1][0]), int(rel_pose[ix * 4 + iy + 1][1])),
                    (int(rel_pose[ix * 4 + iy + 2][0]), int(rel_pose[ix * 4 + iy + 2][1])), colors[ix], 2)
        
        return rel_pose

    def close(self):
        return modelbox.Status()
    
    def data_pre(self, data_context):
        return modelbox.Status()

    def data_post(self, data_context):
        return modelbox.Status()
