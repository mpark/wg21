# MPark.WG21
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
#
# Build-time Pandoc driver (cmake -P). Inputs via -D:
#   PANDOC, SRC, OUT, VENV_BIN, FORMAT, DATA_DIR, PYTHON

foreach(_required PANDOC SRC OUT FORMAT DATA_DIR)
  if(NOT DEFINED ${_required})
    message(FATAL_ERROR "render.cmake: ${_required} is required")
  endif()
endforeach()

# venv first on PATH so pandoc's filters resolve python3 (with panflute) via
# their shebang. Unix-only for now.
get_filename_component(_pandoc_dir "${PANDOC}" DIRECTORY)
set(_prefix "${_pandoc_dir}")
if(DEFINED VENV_BIN AND NOT VENV_BIN STREQUAL "")
  set(_prefix "${VENV_BIN}:${_prefix}")
endif()
set(ENV{PATH} "${_prefix}:$ENV{PATH}")

# srefs.defs (stable-reference link defs) is concatenated before the source
# so definitions in the user's file take precedence, matching base.mk.
set(_args "")
if(EXISTS "${DATA_DIR}/srefs.defs")
  list(APPEND _args "${DATA_DIR}/srefs.defs")
endif()
list(APPEND _args "${SRC}"
  -o "${OUT}"
  "--data-dir=${DATA_DIR}"
  -M "data-dir=${DATA_DIR}"
  -d doc -d formatting)

# Bridge the source's front-matter toc-depth into --toc-depth (html only;
# pandoc ignores the front-matter value otherwise).
if(FORMAT STREQUAL "html")
  if(NOT DEFINED PYTHON)
    message(FATAL_ERROR "render.cmake: PYTHON is required for html output")
  endif()
  execute_process(
    COMMAND "${PYTHON}" "${DATA_DIR}/toc-depth.py"
    INPUT_FILE "${SRC}"
    OUTPUT_VARIABLE _toc_depth
    OUTPUT_STRIP_TRAILING_WHITESPACE
    RESULT_VARIABLE _rc)
  if(NOT _rc EQUAL 0)
    message(FATAL_ERROR "render.cmake: toc-depth.py failed for ${SRC} (exit ${_rc})")
  endif()
  if(_toc_depth)
    list(APPEND _args --toc-depth ${_toc_depth})
  endif()
endif()

execute_process(
  COMMAND "${PANDOC}" ${_args}
  RESULT_VARIABLE _rc)
if(NOT _rc EQUAL 0)
  message(FATAL_ERROR "render.cmake: pandoc failed for ${SRC} -> ${OUT} (exit ${_rc})")
endif()
