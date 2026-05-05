cmake_minimum_required(VERSION 3.8)
project(husky_ur5_cleaner)

find_package(ament_cmake REQUIRED)

install(DIRECTORY urdf launch rviz config meshes worlds 
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
