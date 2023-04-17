
#print_component_title(file_loader)

set(SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/file_loader.cpp)
set(HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/include/file_loader.hpp)

add_library(file_loader SHARED ${SOURCES} ${HEADERS})
add_library(viper::file_loader ALIAS file_loader)

set(VIPER_GENERATED_DIR ${CMAKE_CURRENT_BINARY_DIR}/generated)
target_generate_product_version(
	file_loader "${VIPER_GENERATED_DIR}"
	NAME file_loader
	VERSION_MAJOR ${VIPER_VERSION_MAJOR}
	VERSION_MINOR ${VIPER_VERSION_MINOR}
	VERSION_PATCH ${VIPER_VERSION_PATCH}
	VERSION_REVISION ${VIPER_VERSION_REVISION}
)
target_generate_export_header(file_loader "${VIPER_GENERATED_DIR}")

target_include_directories(file_loader PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include ${VIPER_GENERATED_DIR})
target_link_libraries(file_loader PUBLIC viper::third_party::json viper::third_party::boost)

set_target_properties(file_loader PROPERTIES FOLDER viper/utilities)
