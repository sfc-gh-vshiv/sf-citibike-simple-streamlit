import streamlit as st
import contextlib
from streamlit.echo import ( _get_initial_indent, _get_indent )
from typing import List
import textwrap
import traceback

@contextlib.contextmanager
def echoExpander(title="Show code"):
    from streamlit import code, warning, empty, source_util, expander
    frame = traceback.extract_stack()[-3]
    filename, start_line = frame.filename, frame.lineno
    with source_util.open_python_file(filename) as source_file:
        source_lines = source_file.readlines()
    initial_indent = _get_initial_indent(source_lines[start_line:])
    lines_to_display: List[str] = []
    for line in source_lines[start_line:]:
        indent = _get_indent(line)
        if indent is not None and indent < initial_indent:
            break
        lines_to_display.append(line)
    code_string = textwrap.dedent("".join(lines_to_display))
    yield
    expander(title).code(code_string, "python")
    
