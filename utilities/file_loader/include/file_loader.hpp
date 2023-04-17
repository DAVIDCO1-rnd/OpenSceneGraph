#ifndef __FILE_LOADER_H__
#define __FILE_LOADER_H__

#include <boost/filesystem.hpp>
#include <vector>
#include <string>

#include "export/file_loader_EXPORT.hpp"
#include "json.hpp"

class FILE_LOADER_EXPORT file_loader
{
  public:
	static nlohmann::json read_json_from_path(boost::filesystem::path path);

	static bool is_file_found_in_path(boost::filesystem::path);

	static bool write_string_to_file(boost::filesystem::path path, const std::string& out_file_content);

	static bool write_int_to_file(boost::filesystem::path path, const int& out_file_content);

	static bool read_file_into_string(boost::filesystem::path path, std::string& in_file_content);

	static bool read_file_into_integer(boost::filesystem::path path, int& in_file_content);

	static bool read_file_into_vector(boost::filesystem::path path, std::vector<float>& data_vec);

	static std::vector<boost::filesystem::path> get_list_files_in_directory(const boost::filesystem::path& root, std::string const& ext);

	static std::vector<boost::filesystem::path> get_list_files_in_directory(const boost::filesystem::path& root);

	static boost::filesystem::path find_file_in_directory(const boost::filesystem::path& root, std::string const& ext);
};

#endif // __FILE_LOADER_H__