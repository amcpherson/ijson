import importlib.util
import os
import pickle
import queue
import sys
import threading
import time

import pytest

try:
    import _interpreters
    import _interpqueues as _queues
except ImportError:
    pytest.skip("No sub-interpreter support", allow_module_level=True)

@pytest.fixture(name="interpreter_id")
def interpreter_id_fixture():
    intp_id = _interpreters.create()
    yield intp_id
    _interpreters.destroy(intp_id)


_UNBOUND_ERROR = 2
_PICKLED = 1

@pytest.fixture(name="queue_id")
def queue_id_fixture():
    maxsize = 0
    queue_id = _queues.create(maxsize, _PICKLED, _UNBOUND_ERROR)
    _queues.bind(queue_id)
    yield queue_id
    _queues.release(queue_id)


def test_ijson_can_be_loaded(interpreter_id):
    execinfo = _interpreters.exec(interpreter_id, 'import ijson')
    assert execinfo is None


def test_ijson_yajl2_backend_can_be_loaded(interpreter_id):
    spec = importlib.util.find_spec("ijson.backends._yajl2")
    if spec is None:
        pytest.skip("yajl2_c is not built")
    execinfo = _interpreters.exec(interpreter_id, 'import ijson')
    assert execinfo is None
    execinfo = _interpreters.exec(interpreter_id, 'ijson.get_backend("yajl2_c")')
    assert execinfo is None


SIMPLE_IJSON_ITEMS_USAGE = f"""
import ijson
import pickle
import _interpqueues as _queues

value_out = next(ijson.items(f'{{value_in}}', prefix=''))
_queues.put(queue_id, pickle.dumps(value_out), {_PICKLED}, {_UNBOUND_ERROR})
"""

def test_ijson_can_run(interpreter_id, queue_id):

    if sys.platform == "win32" and os.getenv("CIBUILDWHEEL", "0") == "1":
        pytest.xfail("Currently failing under cibuildwheel@win32")

    VALUE = 43
    _interpreters.set___main___attrs(interpreter_id, {"queue_id": queue_id, "value_in": VALUE}, restrict=True)

    def ijson_in_subinterpreter():
        execinfo = _interpreters.exec(interpreter_id, SIMPLE_IJSON_ITEMS_USAGE)
        assert execinfo is None

    thread = threading.Thread(target=ijson_in_subinterpreter)
    thread.start()

    delay = 10 / 1000
    while True:
        try:
            result_tuple = _queues.get(queue_id)
            result = pickle.loads(result_tuple[0])
            break
        except queue.Empty:
            time.sleep(delay)

    thread.join()
    assert result == VALUE
