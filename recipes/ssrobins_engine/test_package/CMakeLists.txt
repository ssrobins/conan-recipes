cmake_minimum_required(VERSION 3.1.2)
project(test_package CXX)

find_package(ssrobins_engine REQUIRED)

include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/global_settings.cmake)

if(ANDROID)
    add_library(${PROJECT_NAME} SHARED)
else()
    add_executable(${PROJECT_NAME})
endif()

target_sources(${PROJECT_NAME} PRIVATE
    main.cpp
)

target_link_libraries(${PROJECT_NAME}
    ssrobins_engine::ssrobins_engine
)
