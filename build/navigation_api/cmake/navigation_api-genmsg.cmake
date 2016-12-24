# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "navigation_api: 1 messages, 0 services")

set(MSG_I_FLAGS "-Inavigation_api:/home/pi/doda_ws/src/navigation_api/msg;-Istd_msgs:/opt/ros/indigo/share/std_msgs/cmake/../msg;-Igeometry_msgs:/home/pi/doda_ws/src/geometry_msgs/msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(navigation_api_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/pi/doda_ws/src/navigation_api/msg/navigation_msg.msg" NAME_WE)
add_custom_target(_navigation_api_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "navigation_api" "/home/pi/doda_ws/src/navigation_api/msg/navigation_msg.msg" ""
)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(navigation_api
  "/home/pi/doda_ws/src/navigation_api/msg/navigation_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/navigation_api
)

### Generating Services

### Generating Module File
_generate_module_cpp(navigation_api
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/navigation_api
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(navigation_api_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(navigation_api_generate_messages navigation_api_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/doda_ws/src/navigation_api/msg/navigation_msg.msg" NAME_WE)
add_dependencies(navigation_api_generate_messages_cpp _navigation_api_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(navigation_api_gencpp)
add_dependencies(navigation_api_gencpp navigation_api_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS navigation_api_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(navigation_api
  "/home/pi/doda_ws/src/navigation_api/msg/navigation_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/navigation_api
)

### Generating Services

### Generating Module File
_generate_module_lisp(navigation_api
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/navigation_api
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(navigation_api_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(navigation_api_generate_messages navigation_api_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/doda_ws/src/navigation_api/msg/navigation_msg.msg" NAME_WE)
add_dependencies(navigation_api_generate_messages_lisp _navigation_api_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(navigation_api_genlisp)
add_dependencies(navigation_api_genlisp navigation_api_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS navigation_api_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(navigation_api
  "/home/pi/doda_ws/src/navigation_api/msg/navigation_msg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/navigation_api
)

### Generating Services

### Generating Module File
_generate_module_py(navigation_api
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/navigation_api
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(navigation_api_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(navigation_api_generate_messages navigation_api_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/pi/doda_ws/src/navigation_api/msg/navigation_msg.msg" NAME_WE)
add_dependencies(navigation_api_generate_messages_py _navigation_api_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(navigation_api_genpy)
add_dependencies(navigation_api_genpy navigation_api_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS navigation_api_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/navigation_api)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/navigation_api
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(navigation_api_generate_messages_cpp std_msgs_generate_messages_cpp)
add_dependencies(navigation_api_generate_messages_cpp geometry_msgs_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/navigation_api)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/navigation_api
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(navigation_api_generate_messages_lisp std_msgs_generate_messages_lisp)
add_dependencies(navigation_api_generate_messages_lisp geometry_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/navigation_api)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/navigation_api\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/navigation_api
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(navigation_api_generate_messages_py std_msgs_generate_messages_py)
add_dependencies(navigation_api_generate_messages_py geometry_msgs_generate_messages_py)
