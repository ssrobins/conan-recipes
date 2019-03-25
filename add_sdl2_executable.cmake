function(add_sdl2_executable target_name)
    add_executable_custom(${target_name})

    if(ANDROID)
        # Stage copy of gradle project for Android build and SDL's Java files
        execute_process(
            COMMAND ${CMAKE_COMMAND} -E copy_directory
                ${CMAKE_SOURCE_DIR}/Android
                ${CMAKE_CURRENT_BINARY_DIR}/Android
            COMMAND ${CMAKE_COMMAND} -E copy_directory
                ${CONAN_SDL2_ROOT}/android
                ${CMAKE_CURRENT_BINARY_DIR}/Android/app/src/main/java/org/libsdl/app
        )

        if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/assets_dontship/Android)
            execute_process(
                COMMAND ${CMAKE_COMMAND} -E copy
                    ${CMAKE_CURRENT_SOURCE_DIR}/assets_dontship/Android/icon_48x48.png
                    ${CMAKE_CURRENT_BINARY_DIR}/Android/app/src/main/res/mipmap-mdpi/ic_launcher.png
                COMMAND ${CMAKE_COMMAND} -E copy
                    ${CMAKE_CURRENT_SOURCE_DIR}/assets_dontship/Android/icon_72x72.png
                    ${CMAKE_CURRENT_BINARY_DIR}/Android/app/src/main/res/mipmap-hdpi/ic_launcher.png
                COMMAND ${CMAKE_COMMAND} -E copy
                    ${CMAKE_CURRENT_SOURCE_DIR}/assets_dontship/Android/icon_96x96.png
                    ${CMAKE_CURRENT_BINARY_DIR}/Android/app/src/main/res/mipmap-xhdpi/ic_launcher.png
                COMMAND ${CMAKE_COMMAND} -E copy
                    ${CMAKE_CURRENT_SOURCE_DIR}/assets_dontship/Android/icon_144x144.png
                    ${CMAKE_CURRENT_BINARY_DIR}/Android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png
                COMMAND ${CMAKE_COMMAND} -E copy
                    ${CMAKE_CURRENT_SOURCE_DIR}/assets_dontship/Android/icon_192x192.png
                    ${CMAKE_CURRENT_BINARY_DIR}/Android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png
                COMMAND ${CMAKE_COMMAND} -E copy
                    ${CMAKE_CURRENT_SOURCE_DIR}/assets_dontship/Android/icon_512x512.png
                    ${CMAKE_CURRENT_BINARY_DIR}/Android/app/src/main/ic_launcher-web.png
            )
        endif()

        # Process files so they include target-specific properties
        configure_file (
            ${CMAKE_SOURCE_DIR}/Android/app/src/main/AndroidManifest.xml
            ${CMAKE_CURRENT_BINARY_DIR}/Android/app/src/main/AndroidManifest.xml
        )
        configure_file (
            ${CMAKE_SOURCE_DIR}/Android/app/build.gradle
            ${CMAKE_CURRENT_BINARY_DIR}/Android/app/build.gradle
        )
        configure_file (
            ${CMAKE_SOURCE_DIR}/Android/templates/MainActivity.java
            ${CMAKE_CURRENT_BINARY_DIR}/Android/app/src/main/java/com/${company}/${target_name}/MainActivity.java
        )
        configure_file (
            ${CMAKE_SOURCE_DIR}/Android/app/src/main/res/values/strings.xml
            ${CMAKE_CURRENT_BINARY_DIR}/Android/app/src/main/res/values/strings.xml
        )

        # Copy native library to Android build location
        add_custom_command(
            TARGET ${target_name}
            POST_BUILD
            COMMAND cmake -E copy
                $<TARGET_FILE:${target_name}>
                ${CMAKE_CURRENT_BINARY_DIR}/Android/app/src/main/jniLibs/${CMAKE_ANDROID_ARCH_ABI}/$<TARGET_FILE_NAME:${target_name}>
            COMMAND sh ./gradlew assembleRelease
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/Android
        )
    endif()
endfunction(add_sdl2_executable)
