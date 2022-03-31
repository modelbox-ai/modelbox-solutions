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

class CollapseHandPose(modelbox.FlowUnit):
    def __init__(self):
        super().__init__()

    def open(self, config):
        return modelbox.Status.StatusCode.STATUS_SUCCESS

    def process(self, data_context):
        in_feat = data_context.input("in_feat")
        out_data = data_context.output("out_data")

        hand_pose_list = []
        for buffer_feat in in_feat:
            feat_data = np.array(buffer_feat.as_object(), copy=False)
            if feat_data is None:
                continue

            feat_data = feat_data.reshape((-1, 2))
            hand_pose_list.append(feat_data)

        hand_pose_data = np.array(hand_pose_list)
        add_buffer = modelbox.Buffer(self.get_bind_device(), hand_pose_data)
        out_data.push_back(add_buffer)
        return modelbox.Status.StatusCode.STATUS_SUCCESS

    def close(self):
        return modelbox.Status()
    
    def data_pre(self, data_context):
        return modelbox.Status()

    def data_post(self, data_context):
        return modelbox.Status()
