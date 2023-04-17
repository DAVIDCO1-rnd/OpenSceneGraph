#include "file_loader.hpp"

#include <boost/regex.hpp>
#include <cassert>
#include <boost/iterator/iterator_facade.hpp>
#include <fstream>
#include <stdexcept>
#include <string>
#include <iostream>

using json = nlohmann::json;

json file_loader::read_json_from_path(boost::filesystem::path path)
{
	std::ifstream input_file(path.string());
	json json;
	if (input_file)
		input_file >> json;

	if (json.is_null()) {
		throw std::runtime_error("json file not loaded");
	}
	return json;
}

bool file_loader::is_file_found_in_path(boost::filesystem::path path)
{
	return boost::filesystem::exists(path);
}

bool file_loader::write_string_to_file(boost::filesystem::path path, const std::string& out_file_content)
{
	if (!is_file_found_in_path(path)) {
		if (path.has_parent_path()) {
			if (!boost::filesystem::exists(path.parent_path()))
				boost::filesystem::create_directory(path.parent_path());
		}
	}

	std::ofstream out(path.string());

	bool result = (bool)(out << out_file_content.c_str());

	out.close();
	return result;
}


bool file_loader::write_int_to_file(boost::filesystem::path path, const int& int_out_file_content)
{
	std::string str_out_file_content = std::to_string(int_out_file_content);
	bool result = write_string_to_file(path, str_out_file_content);
	return result;
}



bool file_loader::read_file_into_string(boost::filesystem::path path, std::string& content)
{
	bool is_found = is_file_found_in_path(path);
	if (!is_found) {
		std::string err_message = "file not found: " + path.string();
		throw std::runtime_error(err_message.c_str());
	}

	std::ifstream in(path.string(), std::ios::in);
	in.seekg(0, std::ios::end);
	content.resize(in.tellg());
	in.seekg(0);
	//in.read(content.data(), content.size());
	in.read(&content[0], content.size()); //david - don't know if this is correct (the line above didn't compile)

	// remove empty lines
	boost::regex empty_line_regex(R"(\n\s*\n)");
	content = boost::regex_replace(content, empty_line_regex, "\n");

	bool read_result = content.size() > 0;
	assert((read_result) && ("empty file: " + path.string()).c_str());
	return read_result;
}

bool file_loader::read_file_into_integer(boost::filesystem::path path, int& int_file_content)
{
	std::string str_file_content;
	bool read_string_result = read_file_into_string(path, str_file_content);
	if (read_string_result == false)
	{
		return read_string_result;
	}
	try
	{
		int_file_content = std::stoi(str_file_content); //will succeed only if there's an integer at prefix of stoi parameter	
	}
	catch (const std::invalid_argument& e)
	{
		std::cerr << "Error: " << e.what() << std::endl;
	}
	
	return true;
}

bool file_loader::read_file_into_vector(boost::filesystem::path path, std::vector<float>& data_vec)
{
	bool is_found = is_file_found_in_path(path);
	if (!is_found) {
		std::string err_message = "file not found: " + path.string();
		throw std::runtime_error(err_message.c_str());
	}

	std::streampos size;
	std::ifstream in(path.string(), std::ios::in);
	in.seekg(0, std::ios::end);
	size = in.tellg();
	in.seekg(0);

	data_vec.reserve(size);
	data_vec.insert(data_vec.begin(), std::istream_iterator<float>(in), std::istream_iterator<float>());

	assert(data_vec.size() > 0);
	return true;
}

boost::filesystem::path file_loader::find_file_in_directory(const boost::filesystem::path& root, std::string const& ext)
{
	if (boost::filesystem::exists(root) && boost::filesystem::is_directory(root)) {
		for (auto const& entry : boost::filesystem::recursive_directory_iterator(root)) {
			if (boost::filesystem::is_regular_file(entry) && entry.path().extension() == ext)
				return entry.path();
		}
	}

	return boost::filesystem::path();
}

std::vector<boost::filesystem::path> file_loader::get_list_files_in_directory(const boost::filesystem::path& root, std::string const& ext)
{
	std::vector<boost::filesystem::path> paths;

	if (boost::filesystem::exists(root) && boost::filesystem::is_directory(root)) {
		for (auto const& entry : boost::filesystem::recursive_directory_iterator(root)) {
			if (boost::filesystem::is_regular_file(entry) && entry.path().extension() == ext)
				paths.emplace_back(entry.path());
		}
	}
	return paths;
}

std::vector<boost::filesystem::path> file_loader::get_list_files_in_directory(const boost::filesystem::path& root)
{
	std::vector<boost::filesystem::path> paths;

	if (boost::filesystem::exists(root) && boost::filesystem::is_directory(root)) {
		for (auto const& entry : boost::filesystem::recursive_directory_iterator(root)) {
			if (boost::filesystem::is_regular_file(entry))
				paths.emplace_back(entry.path());
		}
	}
	return paths;
}