include(GenerateExportHeader)

# generate headers containing import/export macros using internal cmake functionality
# and adds them to a certain target
#
# Usage:
# 	target_generate_export_header(engine "${VIPER_GENERATED_DIR}")
#
# Args:
#	TARGET_NAME		- target to generate files for
#	EXPORT_LOCATION	- location for creating files in
#
function(target_generate_export_header TARGET_NAME EXPORT_LOCATION)
	string(TOUPPER ${TARGET_NAME} TARGET_NAME_UPPERCASE)
	string(TOLOWER ${TARGET_NAME} TARGET_NAME_LOWERCASE)
	set(EXPORT_MACRO_NAME "${TARGET_NAME_UPPERCASE}_EXPORT")
	set(EXPORT_FILE_NAME "${TARGET_NAME_LOWERCASE}_EXPORT.hpp")

	generate_export_header(
		${TARGET_NAME}
		BASE_NAME
		"${TARGET_NAME_UPPERCASE}"
		EXPORT_MACRO_NAME
		"${EXPORT_MACRO_NAME}"
		EXPORT_FILE_NAME
		"${EXPORT_LOCATION}/export/${EXPORT_FILE_NAME}"
	)

	if(VIPER_CONFIG_VERBOSE)
		message("")
		message(STATUS target_generate_export_header:)
		message(STATUS ------------------------------)
		message(STATUS BASE_NAME: ${TARGET_NAME_UPPERCASE})
		message(STATUS EXPORT_MACRO_NAME: ${EXPORT_MACRO_NAME})
		message(STATUS EXPORT_FILE_NAME: ${EXPORT_FILE_NAME})
		message(STATUS EXPORT_LOCATION: ${EXPORT_LOCATION}/export/${EXPORT_FILE_NAME})
		message("")
	else()

	endif()
endfunction()
