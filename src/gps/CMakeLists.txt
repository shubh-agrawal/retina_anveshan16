cmake_minimum_required(VERSION 2.8.3)
project(gpsdoda)

# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
# find_package(PythonLibs REQUIRED)


include_directories(${catkin_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS} src)

find_package(catkin REQUIRED COMPONENTS message_generation rospy std_msgs)

catkin_package(
	CATKIN_DEPENDS rospy roscpp std_msgs geometry_msgs INCLUDE_DIRS src)

#add_executable(gps src/publisher.py)
#set_target_properties(gps PROPERTIES LINKER_LANGUAGE python)
#target_link_libraries(gps ${catkin_LIBRARIES} ${PYTHON_LIBRARIES})
#add_dependencies(gps roscpp rospy std_msgs geometry_msgs)


