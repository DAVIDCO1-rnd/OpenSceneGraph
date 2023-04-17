# This function uses VersionInfo.in template file and VersionResource.rc file
# to generate WIN32 resource with version information and general resource strings.
#
# Usage:
#   target_generate_product_version(
#     SomeOutputResourceVariable
#     NAME MyGreatProject
#     VERSION_MAJOR 2
#     VERSION_MINOR 3
#     VERSION_PATCH ${BUILD_COUNTER}
#     VERSION_REVISION ${BUILD_REVISION}
#   )
# where BUILD_COUNTER and BUILD_REVISION could be values from your CI server.
#
# You can use generated resource for your executable targets:
#   add_executable(target-name ${target-files} ${SomeOutputResourceVariable})
#
# You can specify resource strings in arguments:
#   NAME               - name of executable (no defaults, ex: Microsoft Word)
#   BUNDLE             - bundle (${NAME} is default, ex: Microsoft Office)
#   VERSION_MAJOR      - 1 is default
#   VERSION_MINOR      - 0 is default
#   VERSION_PATCH      - 0 is default
#   VERSION_REVISION   - 0 is default
#   COMMENTS           - ${NAME} v${VERSION_MAJOR}.${VERSION_MINOR} is default
#   ORIGINAL_FILENAME  - ${NAME} is default
#   VIPER_NAME      - ${NAME} is default
#   FILE_DESCRIPTION   - ${NAME} is default
# 	LOCATION	   	   - ${CMAKE_CURRENT_BINARY_DIR} is default
function(target_generate_product_version LIBRARY_NAME LOCATION)
	set(options)
	set(oneValueArgs
		NAME
		BUNDLE
		VERSION_MAJOR
		VERSION_MINOR
		VERSION_PATCH
		VERSION_REVISION
		COMMENTS
		ORIGINAL_FILENAME
		VIPER_NAME
		FILE_DESCRIPTION
	)
	set(multiValueArgs)

	cmake_parse_arguments(
		PRODUCT
		"${options}"
		"${oneValueArgs}"
		"${multiValueArgs}"
		${ARGN}
	)

	if(NOT PRODUCT_BUNDLE OR "${PRODUCT_BUNDLE}" STREQUAL "")
		set(PRODUCT_BUNDLE "${PRODUCT_NAME}")
	endif()

	if(NOT (PRODUCT_VERSION_MAJOR EQUAL 0) AND (NOT PRODUCT_VERSION_MAJOR OR "${PRODUCT_VERSION_MAJOR}" STREQUAL ""))
		set(PRODUCT_VERSION_MAJOR 1)
	endif()
	if(NOT
	   PRODUCT_VERSION_MINOR
	   EQUAL
	   0
	   AND (NOT PRODUCT_VERSION_MINOR OR "${PRODUCT_VERSION_MINOR}" STREQUAL "")
	)
		set(PRODUCT_VERSION_MINOR 0)
	endif()
	if(NOT
	   PRODUCT_VERSION_PATCH
	   EQUAL
	   0
	   AND (NOT PRODUCT_VERSION_PATCH OR "${PRODUCT_VERSION_PATCH}" STREQUAL "")
	)
		set(PRODUCT_VERSION_PATCH 0)
	endif()
	if(NOT
	   PRODUCT_VERSION_REVISION
	   EQUAL
	   0
	   AND (NOT PRODUCT_VERSION_REVISION OR "${PRODUCT_VERSION_REVISION}" STREQUAL "")
	)
		set(PRODUCT_VERSION_REVISION 0)
	endif()

	if(NOT PRODUCT_COMMENTS OR "${PRODUCT_COMMENTS}" STREQUAL "")
		set(PRODUCT_COMMENTS "${PRODUCT_NAME} v${PRODUCT_VERSION_MAJOR}.${PRODUCT_VERSION_MINOR}")
	endif()
	if(NOT PRODUCT_ORIGINAL_FILENAME OR "${PRODUCT_ORIGINAL_FILENAME}" STREQUAL "")
		set(PRODUCT_ORIGINAL_FILENAME "${PRODUCT_NAME}")
	endif()
	if(NOT PRODUCT_VIPER_NAME OR "${PRODUCT_VIPER_NAME}" STREQUAL "")
		set(PRODUCT_VIPER_NAME "${PRODUCT_NAME}")
	endif()
	if(NOT PRODUCT_FILE_DESCRIPTION OR "${PRODUCT_FILE_DESCRIPTION}" STREQUAL "")
		set(PRODUCT_FILE_DESCRIPTION "${PRODUCT_NAME}")
	endif()

	set(VIPER_VERSION_H_FILENAME_OUT version.hpp)

	set(VIPER_VERSION_H_OUT ${LOCATION}/version/version.hpp)
	set(VIPER_VERSION_RC_OUT ${LOCATION}/version/version.rc)

	# adding a version.hpp file
	configure_file(${CMAKE_SOURCE_DIR}/cmake/utils/version/version_info.hpp.in ${VIPER_VERSION_H_OUT} @ONLY)

	# adding a version.rc file
	configure_file(${CMAKE_SOURCE_DIR}/cmake/utils/version/version_resource.rc ${VIPER_VERSION_RC_OUT} @ONLY)

	list(
		APPEND
		OUTFILES
		${VIPER_VERSION_H_OUT}
		${VIPER_VERSION_RC_OUT}
	)

	if(VIPER_CONFIG_VERBOSE)
		message("")
		message(STATUS generate_product_version:)
		message(STATUS -------------------------)
		message(STATUS "NAME: ${PRODUCT_NAME}")
		message(STATUS "LOCATION: ${LOCATION}")
		message(STATUS "VERSION_H_FILENAME_OUT: ${VIPER_VERSION_H_FILENAME_OUT}")
		message(STATUS "OUTFILES: ${OUTFILES}")
		message("")
	else()

	endif()

	target_sources(${LIBRARY_NAME} PRIVATE ${VIPER_VERSION_H_OUT} ${VIPER_VERSION_RC_OUT})
endfunction()
