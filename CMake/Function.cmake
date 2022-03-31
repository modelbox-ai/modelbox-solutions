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

macro(subdirlist result dir)
  file(GLOB children RELATIVE ${dir} ${dir}/*)
  set (file ${ARGN})
  set(dirs "")
  foreach(child ${children})
    if(IS_DIRECTORY ${dir}/${child})
        if(NOT ${file} STREQUAL "")
            if(NOT EXISTS ${dir}/${child}/${file})
                CONTINUE()
            endif()
        endif()
        set(dirs ${dirs} ${child})
    endif()
  endforeach()
  set(${result} ${dirs})
endmacro()

function (exclude_files_from_dir_in_list result filelist excludedir)
  foreach (ITR ${filelist})
    if ("${ITR}" MATCHES "(.*)${excludedir}(.*)")                   
      list (REMOVE_ITEM filelist ${ITR})                              
    endif ("${ITR}" MATCHES "(.*)${excludedir}(.*)")

  endforeach(ITR)
  set(${result} ${filelist} PARENT_SCOPE)                          
endfunction (exclude_files_from_dir_in_list)

function (group_source_test_files source test test_pattern filelist)
  set(list_var "${ARGN}")
  foreach (ITR ${filelist} ${list_var})
    if ("${ITR}" MATCHES "(.*)${test_pattern}(.*)")                   
      list (APPEND test_list ${ITR})                 
    else()
      list (APPEND source_list ${ITR})              
    endif ()
  endforeach(ITR) 
  set(${source} ${source_list} PARENT_SCOPE)  
  set(${test} ${test_list} PARENT_SCOPE)  
endfunction(group_source_test_files)
