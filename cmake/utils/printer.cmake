# # prints a title
# function(print_title msg)
# 	if(VIPER_CONFIG_VERBOSE)
# 		message("")
# 		message("=====================================================")
# 		message(${msg})
# 		message("=====================================================")
# 		message("")
# 	else()
# 		message(STATUS "")
# 		message(STATUS ${msg})
# 		message(STATUS "---------------------")
# 	endif()
# endfunction()

# # prints a subtitle
# function(print_status_title)
# 	if(VIPER_CONFIG_VERBOSE)
# 		message("")
# 		message(STATUS "-----------------------------------------------------")
# 		message(STATUS ${msg})
# 		message(STATUS "-----------------------------------------------------")
# 		message("")
# 	endif()
# endfunction()

# # prints a title for each component
# function(print_component_title msg)
# 	if(VIPER_CONFIG_VERBOSE)
# 		print_status_title(${msg})
# 	else()
# 		message(STATUS "Added subdirectory: ${msg}")
# 	endif()
# endfunction()

# function(message)
# 	list(POP_FRONT ARGN MESSAGE_TYPE)

# 	if(NOT VIPER_MESSAGE_QUIET)
# 		_message(${MESSAGE_TYPE} "${ARGN}") # calls overridden function
# 	endif()
# endfunction()
