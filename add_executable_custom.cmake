function(add_executable_custom target_name)
    if(ANDROID)
        add_library(${target_name} SHARED)
    else()
        add_executable(${target_name})
    endif()

    if(APPLE)
        set_target_properties(${target_name}
            PROPERTIES
            MACOSX_BUNDLE_BUNDLE_VERSION "${version_major}.${version_minor}.${version_patch}"
            MACOSX_BUNDLE_SHORT_VERSION_STRING "${version_major}.${version_minor}.${version_patch}"
            XCODE_ATTRIBUTE_CODE_SIGN_IDENTITY "${xcode_code_sign_identity}"
            XCODE_ATTRIBUTE_DEVELOPMENT_TEAM "${xcode_dev_team}"
        )
    endif()

    if(IOS)
        if(${ENABLE_BITCODE})
            set(xcode_bitcode YES)
        else()
            set(xcode_bitcode NO)
        endif()

        set_target_properties(${target_name}
            PROPERTIES
            MACOSX_BUNDLE TRUE
            XCODE_ATTRIBUTE_ASSETCATALOG_COMPILER_APPICON_NAME "AppIcon"
            XCODE_ATTRIBUTE_ASSETCATALOG_COMPILER_LAUNCHIMAGE_NAME "LaunchImage"
            XCODE_ATTRIBUTE_ENABLE_BITCODE "${xcode_bitcode}"
            XCODE_ATTRIBUTE_INSTALL_PATH "$(LOCAL_APPS_DIR)"
            XCODE_ATTRIBUTE_IPHONEOS_DEPLOYMENT_TARGET "${IOS_DEPLOYMENT_TARGET}"
            XCODE_ATTRIBUTE_TARGETED_DEVICE_FAMILY "1,2" # 1=iPhone/iPod, 2=iPad
            RESOURCE "${icons}"
        )
    else(APPLE)
        set_target_properties(${target_name}
            PROPERTIES
            XCODE_ATTRIBUTE_CODE_SIGN_STYLE "Manual"
        )
    endif()
endfunction(add_executable_custom)