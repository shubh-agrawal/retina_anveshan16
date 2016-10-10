cmake_minimum_required(VERSION 2.8.3)
project(nrfcomm)

# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
# find_package(PythonLibs REQUIRED)


include_directories(${catkin_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS} src)

find_package(catkin REQUIRED COMPONENTS
    message_generation
    rospy 
    std_msgs
    geometry_msgs
    navigation_api
) 

catkin_package(
        CATKIN_DEPENDS rospy roscpp std_msgs navigation_api INCLUDE_DIRS src
)

catkin_package()
