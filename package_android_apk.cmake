function(gradle_build component)
    if(component)
        set(package_name ${component})
    else()
        set(package_name ${CPACK_PACKAGE_NAME})
    endif()

    message("\n\nBuilding APK for ${package_name}")

    execute_process(
        COMMAND sh ./gradlew assemble${CPACK_BUILD_CONFIG}
        WORKING_DIRECTORY ${CPACK_TEMPORARY_DIRECTORY}/${component}/Android
        RESULT_VARIABLE gradle_result
    )
    if(gradle_result)
        message(FATAL_ERROR "Gradle error")
    endif()

    file(GLOB_RECURSE apk_files
        "${CPACK_TEMPORARY_DIRECTORY}/${component}/Android/app/build/outputs/apk/*.apk"
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
