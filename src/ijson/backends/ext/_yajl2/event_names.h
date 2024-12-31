/*
 * Event name singletons for ijson's C backend
 *
 * Contributed by Rodrigo Tobar <rtobar@icrar.org>
 *
 * ICRAR - International Centre for Radio Astronomy Research
 * (c) UWA - The University of Western Australia, 2024
 * Copyright by UWA (in the framework of the ICRAR)
 */

#ifndef EVENT_NAMES_H
#define EVENT_NAMES_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

/*
 * A structure (and variable) holding utf-8 strings with the event names
 * This way we avoid calculating them every time, and we can compare them
 * via direct equality comparison instead of via strcmp.
 */
typedef struct _event_names {
	PyObject *null_ename;
	PyObject *boolean_ename;
	PyObject *integer_ename;
	PyObject *double_ename;
	PyObject *number_ename;
	PyObject *string_ename;
	PyObject *start_map_ename;
	PyObject *map_key_ename;
	PyObject *end_map_ename;
	PyObject *start_array_ename;
	PyObject *end_array_ename;
} enames_t;

#define FOR_EACH_EVENT(f)                \
   f(null_ename, "null");                \
   f(boolean_ename, "boolean");          \
   f(integer_ename, "integer");          \
   f(double_ename, "double");            \
   f(number_ename, "number");            \
   f(string_ename, "string");            \
   f(start_map_ename, "start_map");      \
   f(map_key_ename, "map_key");          \
   f(end_map_ename, "end_map");          \
   f(start_array_ename, "start_array");  \
   f(end_array_ename, "end_array");

#endif /* EVENT_NAMES_H */