############################################
# boost libraries
############################################

set(Boost_Dir $ENV{Boost_Dir})
set(Boost_USE_STATIC_LIBS ON)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)
set(Boost_NO_SYSTEM_PATH ON)

if(WIN32 AND NOT MSVC)
	set(Boost_COMPILER vc142)
endif()

find_package(
	Boost
	REQUIRED
	thread
	filesystem
	regex
)

# create alias library
add_library(boost_alias_lib INTERFACE)
target_link_libraries(boost_alias_lib INTERFACE ${Boost_LIBRARIES})
add_library(viper::third_party::boost ALIAS boost_alias_lib)

if(VIPER_CONFIG_VERBOSE)
	#print_status_title("Boost libraries")
	message(STATUS Boost_Dir: "${Boost_Dir}")
	message(STATUS Boost_USE_STATIC_LIBS: "${Boost_USE_STATIC_LIBS}")
	message(STATUS Boost_USE_MULTITHREADED: "${Boost_USE_MULTITHREADED}")
	message(STATUS Boost_USE_STATIC_RUNTIME: "${Boost_USE_STATIC_RUNTIME}")
	message(STATUS Boost_NO_SYSTEM_PATH: "${Boost_NO_SYSTEM_PATH}")
	message("")
endif()

############################################
# json libraries
############################################

add_library(json_alias_lib INTERFACE)
target_include_directories(json_alias_lib INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/json)
add_library(viper::third_party::json ALIAS json_alias_lib)

if(VIPER_CONFIG_VERBOSE)
	#print_status_title("Json header")
	message(STATUS "JSON_INCLUDE_DIRECTORY: ${CMAKE_CURRENT_SOURCE_DIR}/json")
	message("")
else()
	message(STATUS "Found nlohmann::json")
endif()