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

from yolox_utils import postprocess

class YoloxPost(modelbox.FlowUnit):
    def __init__(self):
        super().__init__()

    def open(self, config):
        self.net_h = config.get_int("net_h", 320)
        self.net_w = config.get_int("net_w", 320)
        self.num_classes = config.get_int("num_classes", 1)
        self.num_grids = int((self.net_h / 32) * (self.net_w / 32)) * (1 + 2 * 2 + 4 * 4)
        self.conf_thre = config.get_float("conf_threshold", 0.3)
        self.nms_thre = config.get_float("iou_threshold", 0.4)
        return modelbox.Status.StatusCode.STATUS_SUCCESS

    def process(self, data_context):
        in_image_bufferlist = data_context.input("in_image")
        in_feat_bufferlist = data_context.input("in_feat")
        
        has_hand_bufferlist = data_context.output("has_hand")
        no_hand_bufferlist = data_context.output("no_hand")

        for image_buffer, feat_buffer in zip(in_image_bufferlist, in_feat_bufferlist):
            width = image_buffer.get("width")
            height = image_buffer.get("height")
            channel = image_buffer.get("channel")

            img_data = np.array(image_buffer.as_object(), copy=False)
            img_data = img_data.reshape(height, width, channel)

            feat_data = np.array(feat_buffer.as_object(), copy=False)
            feat_data = feat_data.reshape((self.num_classes + 5, self.num_grids)).transpose()

            bboxes = postprocess(feat_data, (self.net_h, self.net_w), (height, width), self.conf_thre, self.nms_thre)

            if bboxes is None:
                image_buffer.set("has_hand", False)
                no_hand_bufferlist.push_back(image_buffer)
            else:
                image_buffer.set("has_hand", True)
                bboxes = bboxes[:, :4].astype(int) # x1,y1,x2,y2
                image_buffer.set("bboxes", bboxes.flatten().tolist())
                has_hand_bufferlist.push_back(image_buffer)

        return modelbox.Status.StatusCode.STATUS_SUCCESS

    def close(self):
        return modelbox.Status()
    
    def data_pre(self, data_context):
        return modelbox.Status()

    def data_post(self, data_context):
        return modelbox.Status()
