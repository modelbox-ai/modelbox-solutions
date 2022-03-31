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


cmake_minimum_required(VERSION 3.10)

set(DOWNLOAD_DIR ${CMAKE_CURRENT_BINARY_DIR}/download)

# predownload solution models
include(ExternalProject)

# downlaod hand_pose_detection model files
if (NOT BUILD_SOLUTION_NAME OR 
    BUILD_SOLUTION_NAME STREQUAL "hand_pose_detection")
    set(MODELS_DIR ${DOWNLOAD_DIR}/hand_pose_detection)

    ExternalProject_Add(
      hand_pose_detection
      URL                 "http://download.modelbox-ai.com/model/hand_pose_detection_models_v1.0.zip"
      SOURCE_DIR          ${MODELS_DIR}
      CONFIGURE_COMMAND   ""
      BUILD_COMMAND       ""
      INSTALL_COMMAND     ""
      TEST_COMMAND        ""
    )

    set(HAND_DETECTION_MODEL_FILE ${MODELS_DIR}/yolox_320x320_nodecode.pt CACHE INTERNAL "")
    set(HAND_POSE_DETECTION_MODEL_FILE ${MODELS_DIR}/hand_pose_256x256.pt CACHE INTERNAL "")
endif()
