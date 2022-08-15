cmake_minimum_required(VERSION 3.17)

project(Project)

add_subdirectory(source)

set_target_properties(ogg PROPERTIES DEBUG_POSTFIX d)
