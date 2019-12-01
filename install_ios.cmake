execute_process(
    COMMAND xcodebuild -workspace @PROJECT_NAME@.xcodeproj/project.xcworkspace -scheme @target_name@ archive -archivePath @component_name@.xcarchive
        RESULT_VARIABLE xcode_archive_result
    )
    if(xcode_archive_result)
        message(FATAL_ERROR "Xcode error")
    endif()

file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/." TYPE DIRECTORY FILES "@CMAKE_BINARY_DIR@/@component_name@.xcarchive")
