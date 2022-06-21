cmake_minimum_required(VERSION 3.1.2)
project(test_package CXX)

find_package(box2d REQUIRED)

add_executable(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    main.cpp
)

target_link_libraries(${PROJECT_NAME}
    box2d::box2d
)
