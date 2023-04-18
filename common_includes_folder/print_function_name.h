#ifndef OSG_PRINT_FUNCTION_NAME
#define OSG_PRINT_FUNCTION_NAME

#include <iostream>

#define PRINT_FUNCTION_NAME TrailFunctions print_details_at_the_beginning_of_function(__FUNCTION__);

class TrailFunctions {
private:
	static int entry_counter;
	const char *function_name;

public:
	TrailFunctions(const char *f) : function_name(f)
	{
		if (entry_counter == 0)
		{
			printf("Entered into %s\n", function_name);
		}
		entry_counter++;

	}


	~TrailFunctions()
	{
		entry_counter--;
		if (entry_counter == 0)
		{
			printf("Exited from %s\n\n", function_name);
		}
	}
};

#ifndef TrailFunctions::entry_counter
int TrailFunctions::entry_counter = 0;
#endif

#endif