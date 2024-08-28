/*
 * _yajl2 backend for ijson
 *
 * Contributed by Rodrigo Tobar <rtobar@icrar.org>
 *
 * ICRAR - International Centre for Radio Astronomy Research
 * (c) UWA - The University of Western Australia, 2016
 * Copyright by UWA (in the framework of the ICRAR)
 */

#include "common.h"
#include "async_reading_generator.h"
#include "basic_parse.h"
#include "basic_parse_async.h"
#include "basic_parse_basecoro.h"
#include "parse.h"
#include "parse_async.h"
#include "parse_basecoro.h"
#include "items.h"
#include "items_async.h"
#include "items_basecoro.h"
#include "kvitems.h"
#include "kvitems_async.h"
#include "kvitems_basecoro.h"

#define MODULE_NAME "_yajl2"

enames_t enames;
PyObject *dot, *item, *dotitem;
PyObject *JSONError;
PyObject *IncompleteJSONError;
PyObject *Decimal;

static PyMethodDef yajl2_methods[] = {
	{NULL, NULL, 0, NULL}        /* Sentinel */
};

static int _yajl2_mod_exec(PyObject *m);

static PyModuleDef_Slot yajl2_slots[] = {
	{Py_mod_exec, _yajl2_mod_exec},
	{0, NULL},
};

PyObject* ijson_return_self(PyObject *self)
{
	Py_INCREF(self);
	return self;
}

PyObject* ijson_return_none(PyObject *self)
{
	Py_RETURN_NONE;
}

/* Module initialization */

/* Support for Python 2/3 */
static struct PyModuleDef moduledef = {
	.m_base = PyModuleDef_HEAD_INIT,
	.m_name = MODULE_NAME,
	.m_doc = "wrapper for yajl2 methods",
	.m_size = 0,
	.m_methods = yajl2_methods,
	.m_slots = yajl2_slots,
};

PyMODINIT_FUNC PyInit__yajl2(void)
{
	return PyModuleDef_Init(&moduledef);
}

static int _yajl2_mod_exec(PyObject *m)
{
#define ADD_TYPE(name, type) \
	{ \
		type.tp_new = PyType_GenericNew; \
		M1_M1(PyType_Ready(&type)); \
		Py_INCREF(&type); \
		PyModule_AddObject(m, name, (PyObject *)&type); \
	}
	ADD_TYPE("basic_parse_basecoro", BasicParseBasecoro_Type);
	ADD_TYPE("basic_parse", BasicParseGen_Type);
	ADD_TYPE("parse_basecoro", ParseBasecoro_Type);
	ADD_TYPE("parse", ParseGen_Type);
	ADD_TYPE("kvitems_basecoro", KVItemsBasecoro_Type);
	ADD_TYPE("kvitems", KVItemsGen_Type);
	ADD_TYPE("items_basecoro", ItemsBasecoro_Type);
	ADD_TYPE("items", ItemsGen_Type);
	ADD_TYPE("_async_reading_iterator", AsyncReadingGeneratorType);
	ADD_TYPE("basic_parse_async", BasicParseAsync_Type);
	ADD_TYPE("parse_async", ParseAsync_Type);
	ADD_TYPE("kvitems_async", KVItemsAsync_Type);
	ADD_TYPE("items_async", ItemsAsync_Type);

	dot = STRING_FROM_UTF8(".", 1);
	item = STRING_FROM_UTF8("item", 4);
	dotitem = STRING_FROM_UTF8(".item", 5);
#define INIT_ENAME(x) enames.x##_ename = STRING_FROM_UTF8(#x, strlen(#x))
	INIT_ENAME(null);
	INIT_ENAME(boolean);
	INIT_ENAME(integer);
	INIT_ENAME(double);
	INIT_ENAME(number);
	INIT_ENAME(string);
	INIT_ENAME(start_map);
	INIT_ENAME(map_key);
	INIT_ENAME(end_map);
	INIT_ENAME(start_array);
	INIT_ENAME(end_array);

	// Import globally-used names
	PyObject *ijson_common = PyImport_ImportModule("ijson.common");
	PyObject *decimal_module = PyImport_ImportModule("decimal");
	M1_N(ijson_common);
	M1_N(decimal_module);

	JSONError = PyObject_GetAttrString(ijson_common, "JSONError");
	IncompleteJSONError = PyObject_GetAttrString(ijson_common, "IncompleteJSONError");
	Decimal = PyObject_GetAttrString(decimal_module, "Decimal");
	M1_N(JSONError);
	M1_N(IncompleteJSONError);
	M1_N(Decimal);

	return 0;
}