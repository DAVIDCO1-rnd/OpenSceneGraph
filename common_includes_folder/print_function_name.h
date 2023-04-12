#ifndef OSG_PRINT_FUNCTION_NAME
#define OSG_PRINT_FUNCTION_NAME
#include <iostream>

#define PRINT_FUNCTION_NAME EntryRaiiObject obj(__FUNCTION__);

struct EntryRaiiObject {
	EntryRaiiObject(const char *f) : function_name(f)
	{ 
		printf("Entered into %s\n", function_name);
	}
	~EntryRaiiObject() 
	{ 
		printf("Exited from %s\n\n", function_name);
	}
	const char *function_name;
};
#endif