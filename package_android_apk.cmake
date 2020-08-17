function(gradle_build component)
    if(component)
        set(package_name ${component})
    else()
        set(package_name ${CPACK_PACKAGE_NAME})
    endif()

    message("\n\nBuilding APK for ${package_name}")

    if(WIN32)
        set(gradle_command gradlew.bat)
        set(gradle_extra_params -Dorg.gradle.daemon.idletimeout=1000)
    else()
        set(gradle_command ./gradlew)
    endif()

    execute_process(
        COMMAND ${gradle_command} assemble${CPACK_BUILD_CONFIG} ${gradle_extra_params}
        WORKING_DIRECTORY ${CPACK_TEMPORARY_DIRECTORY}/${component}
        RESULT_VARIABLE gradle_result
    )
    if(gradle_result)
        message(FATAL_ERROR "Gradle error")
    endif()

    file(GLOB_RECURSE apk_files
        "${CPACK_TEMPORARY_DIRECTORY}/${component}/app/build/outputs/apk/*.apk"
    )
    file(COPY ${apk_files} DESTINATION ${CPACK_PACKAGE_DIRECTORY})
endfunction(gradle_build)


if(CPACK_COMPONENTS_ALL)
    foreach(component ${CPACK_COMPONENTS_ALL})
        gradle_build(${component})
    endforeach()
else()
    gradle_build("")
endif()
