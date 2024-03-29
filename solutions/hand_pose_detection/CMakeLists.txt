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

set(UNIT_COMPONENT "hand_pose_detection")

set(RELEASE_PACKAGE_DIR_LIB ${MODELBOX_SOLUTIONS_INSTALL_DIR}/${UNIT_COMPONENT})
set(RELEASE_PACKAGE_DIR_PYTHON ${MODELBOX_SOLUTIONS_INSTALL_DIR}/${UNIT_COMPONENT})
set(RELEASE_PACKAGE_DIR_MODEL ${MODELBOX_SOLUTIONS_INSTALL_DIR}/${UNIT_COMPONENT})
set(RELEASE_PACKAGE_DIR_GRAPH ${MODELBOX_SOLUTIONS_INSTALL_DIR}/graphs)

if(${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_BINARY_DIR})
    message(FATAL_ERROR "cannot build the project in the source directory! Out-of-source build is enforced!")
endif()

subdirlist(SUBDIRS ${CMAKE_CURRENT_SOURCE_DIR} "CMakeLists.txt")

foreach(subdir ${SUBDIRS})
   add_subdirectory(${subdir})
endforeach()
