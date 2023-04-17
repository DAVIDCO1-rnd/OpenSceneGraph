#ifndef OSG_PRINT_FUNCTION_NAME
#define OSG_PRINT_FUNCTION_NAME

#include <iostream>
#include <boost/dll/runtime_symbol_info.hpp>
#include <file_loader.hpp>

#define PRINT_FUNCTION_NAME TrailFunctions print_details_at_the_beginning_of_function(__FUNCTION__);

class TrailFunctions {
private:
	int entry_counter;
	const char *function_name;
	boost::filesystem::path counter_file_path;

public:
	TrailFunctions(const char *f) : function_name(f)
	{
		counter_file_path = boost::dll::program_location().parent_path().parent_path().parent_path().parent_path().parent_path().append("debug_print_configuration").append("counter_index.txt");
		//std::cout << "counter_file_path = " << counter_file_path.string() << std::endl;
		file_loader::read_file_into_integer(counter_file_path, entry_counter);

		if (entry_counter == 0)
		{
			printf("Entered into %s\n", function_name);
		}
		entry_counter++;
		file_loader::write_int_to_file(counter_file_path, entry_counter);
	}
	~TrailFunctions()
	{
		entry_counter--;
		file_loader::write_int_to_file(counter_file_path, entry_counter);
		if (entry_counter == 0)
		{
			printf("Exited from %s\n\n", function_name);
		}
	}
};

#endif