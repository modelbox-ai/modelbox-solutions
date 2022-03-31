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

class ExpandBox(modelbox.FlowUnit):
    def __init__(self):
        super().__init__()

    def open(self, config):
        return modelbox.Status.StatusCode.STATUS_SUCCESS

    def process(self, data_context):
        in_data_list = data_context.input("in_data")
        out_image_list = data_context.output("roi_image")

        for in_buffer in in_data_list:
            width = in_buffer.get("width")
            height = in_buffer.get("height")
            channel = in_buffer.get("channel")

            img = np.array(in_buffer.as_object(), dtype=np.uint8)
            img = img.reshape(height, width, channel)

            bboxes = in_buffer.get("bboxes")
            bboxes = np.array(bboxes).reshape(-1, 4)
            for box in bboxes:
                img_roi = self.crop_bbox_img(box, img)
                h, w, c = img_roi.shape 
                img_roi = img_roi.flatten()
                add_buffer = modelbox.Buffer(self.get_bind_device(), img_roi)
                add_buffer.copy_meta(in_buffer)
                add_buffer.set("pix_fmt", "rgb")
                add_buffer.set("width", w)
                add_buffer.set("height", h)
                add_buffer.set("width_stride", w)
                add_buffer.set("height_stride", h)
                out_image_list.push_back(add_buffer)
        return modelbox.Status.StatusCode.STATUS_SUCCESS

    def crop_bbox_img(self, bbox, image):
        h, w, c = image.shape
        x1, y1, x2, y2 = self.expand_bbox(bbox, (h, w))
        bbox_img = image[y1:y2, x1:x2, :].copy()
        return bbox_img

    def expand_bbox(self, bbox, image_shape, ratio=1.2):
        h, w, = image_shape
        x1, y1, x2, y2 = bbox
        new_w = int((x2 - x1) * ratio)
        new_h = int((y2 - y1) * ratio)
        c_x = int((x2 + x1) / 2)
        c_y = int((y2 + y1) / 2)
        new_x1 = max(0, int(c_x - new_w / 2))
        new_x2 = min(int(c_x + new_w / 2), w)
        new_y1 = max(0, int(c_y - new_h / 2))
        new_y2 = min(int(c_y + new_h / 2), h)
        new_bbox = [new_x1, new_y1, new_x2, new_y2]
        return new_bbox

    def close(self):
        return modelbox.Status()
    
    def data_pre(self, data_context):
        return modelbox.Status()

    def data_post(self, data_context):
        return modelbox.Status()
