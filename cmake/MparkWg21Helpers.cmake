# MPark.WG21
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
#
# Defines wg21_add_paper() + the shared staging/generation targets. Included by
# FindMparkWg21.cmake. Set before including:
#   MparkWg21_DATA_SRC       - the framework's source data/ directory
#   MparkWg21_RENDER_SCRIPT  - path to render.cmake

# find_package() re-runs its module on each call; define everything once.
if(COMMAND wg21_add_paper)
  return()
endif()

# FindPandoc.cmake is shipped alongside this file.
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")

# Transitive tools (raw find_package; the caller satisfies them). The Python
# modules are asserted, not provisioned -- that's the caller's job. Failures
# are collected in MparkWg21_TOOLS_MISSING: when included from FindMparkWg21
# (which sets _MparkWg21_from_find_module) they become a standard not-found
# result honoring REQUIRED/QUIET; a direct add_subdirectory fails here.
if(MparkWg21_FIND_QUIETLY)
  set(_mparkwg21_quiet QUIET)
else()
  set(_mparkwg21_quiet)
endif()

set(MparkWg21_TOOLS_MISSING "")
set(_mparkwg21_py_err "")

find_package(Python3 3.10 ${_mparkwg21_quiet} COMPONENTS Interpreter)
if(Python3_FOUND)
  set(_mparkwg21_modules panflute bs4 lxml requests yaml)
  list(JOIN _mparkwg21_modules ", " _mparkwg21_imports)
  execute_process(
    COMMAND "${Python3_EXECUTABLE}" -c "import ${_mparkwg21_imports}"
    RESULT_VARIABLE _mparkwg21_py_rc
    ERROR_VARIABLE _mparkwg21_py_err)
  if(NOT _mparkwg21_py_rc EQUAL 0)
    # No semicolons here: the string passes through FPHSA's argument parsing.
    list(APPEND MparkWg21_TOOLS_MISSING
      "Python modules for ${Python3_EXECUTABLE} (need ${_mparkwg21_imports} -- \
try `pip install panflute beautifulsoup4 lxml requests pyyaml`)")
  endif()
else()
  list(APPEND MparkWg21_TOOLS_MISSING "Python3 >= 3.10")
endif()

find_package(Pandoc 3.9.0.2 ${_mparkwg21_quiet})
if(NOT Pandoc_FOUND)
  list(APPEND MparkWg21_TOOLS_MISSING "Pandoc >= 3.9.0.2 (hint: Pandoc_ROOT)")
endif()

if(MparkWg21_TOOLS_MISSING)
  if(_MparkWg21_from_find_module)
    return()
  endif()
  list(JOIN MparkWg21_TOOLS_MISSING "\n  " _mparkwg21_missing)
  message(FATAL_ERROR
    "MparkWg21: missing tools:\n  ${_mparkwg21_missing}\n${_mparkwg21_py_err}")
endif()

set(MparkWg21_RENDER_SCRIPT "${MparkWg21_RENDER_SCRIPT}" CACHE INTERNAL "")
# Unlike find_program results, FindPython3's Python3_EXECUTABLE is scope-local;
# snapshot it so wg21_add_paper sees it from any call site.
set(MparkWg21_PYTHON "${Python3_EXECUTABLE}" CACHE INTERNAL "")

# Staged data dir in the build tree: pandoc's --data-dir must hold the
# committed data/ files plus the generated reference files. Staging there keeps
# the source/install read-only; one shared location means one stage + one fetch
# per build.
set(MparkWg21_STAGED_DATA_DIR "${CMAKE_BINARY_DIR}/mpark-wg21/data"
    CACHE INTERNAL "wg21 staged data dir")
set(_sentinel "${MparkWg21_STAGED_DATA_DIR}/metadata.yaml")
set(_csl      "${MparkWg21_STAGED_DATA_DIR}/csl.json")
set(_srefs    "${MparkWg21_STAGED_DATA_DIR}/srefs.json")
set(_srefs_defs "${MparkWg21_STAGED_DATA_DIR}/srefs.defs")

# The copied metadata.yaml is the sentinel for the bulk copy. Deliberately no
# DEPENDS: staging runs once, edits under data/ need a fresh build tree.
add_custom_command(
  OUTPUT "${_sentinel}"
  COMMAND "${CMAKE_COMMAND}" -E copy_directory
          "${MparkWg21_DATA_SRC}" "${MparkWg21_STAGED_DATA_DIR}"
  COMMENT "Staging wg21 data directory"
  VERBATIM)

# Generated reference data (network-backed; fetched once). Paths go in as
# positional args ($1..) to keep them out of the `bash -c` string.
add_custom_command(
  OUTPUT "${_csl}"
  COMMAND bash -c "\"$1\" \"$2\" > \"$3\""
          wg21 "${Python3_EXECUTABLE}" "${MparkWg21_DATA_SRC}/refs.py" "${_csl}"
  DEPENDS "${MparkWg21_DATA_SRC}/refs.py" "${_sentinel}"
  COMMENT "Fetching citation reference data (network)"
  VERBATIM)

add_custom_command(
  OUTPUT "${_srefs}"
  COMMAND bash -c "\"$1\" \"$2\" > \"$3\""
          wg21 "${Python3_EXECUTABLE}" "${MparkWg21_DATA_SRC}/srefs.py" "${_srefs}"
  DEPENDS "${MparkWg21_DATA_SRC}/srefs.py" "${_sentinel}"
  COMMENT "Fetching stable-name reference data (network)"
  VERBATIM)

add_custom_command(
  OUTPUT "${_srefs_defs}"
  COMMAND bash -c "\"$1\" \"$2\" < \"$3\" > \"$4\""
          wg21 "${Python3_EXECUTABLE}" "${MparkWg21_DATA_SRC}/srefs-md.py"
          "${_srefs}" "${_srefs_defs}"
  DEPENDS "${MparkWg21_DATA_SRC}/srefs-md.py" "${_srefs}" "${_sentinel}"
  COMMENT "Generating stable-name markdown"
  VERBATIM)

add_custom_target(wg21_data DEPENDS "${_sentinel}" "${_csl}" "${_srefs}" "${_srefs_defs}")

# wg21_add_paper(<name>
#   [SOURCE <file>]    default: <name>.md in the caller's dir
#   [FORMATS ...]      default: html
#   [OUTDIR <dir>]     default: caller's CMAKE_CURRENT_BINARY_DIR
#   [ALL])             attach to the default build target
function(wg21_add_paper name)
  cmake_parse_arguments(PARSE_ARGV 1 ARG
    "ALL"
    "SOURCE;OUTDIR"
    "FORMATS")
  if(ARG_UNPARSED_ARGUMENTS)
    message(FATAL_ERROR "wg21_add_paper(${name}): unexpected arguments: "
                        "${ARG_UNPARSED_ARGUMENTS}")
  endif()

  if(NOT ARG_SOURCE)
    set(ARG_SOURCE "${CMAKE_CURRENT_SOURCE_DIR}/${name}.md")
  endif()
  if(NOT ARG_FORMATS)
    set(ARG_FORMATS html)
  endif()
  if(NOT ARG_OUTDIR)
    set(ARG_OUTDIR "${CMAKE_CURRENT_BINARY_DIR}")
  endif()

  get_filename_component(_venv_bin "${MparkWg21_PYTHON}" DIRECTORY)
  set(_data "${MparkWg21_STAGED_DATA_DIR}")
  # Render from the source's directory so relative resources (e.g. images)
  # resolve, as they do when running make from a paper directory.
  get_filename_component(_src_dir "${ARG_SOURCE}" DIRECTORY)

  set(_outputs "")
  foreach(fmt IN LISTS ARG_FORMATS)
    set(_out "${ARG_OUTDIR}/${name}.${fmt}")
    add_custom_command(
      OUTPUT "${_out}"
      COMMAND "${CMAKE_COMMAND}"
              "-DPANDOC=${Pandoc_EXECUTABLE}"
              "-DPYTHON=${MparkWg21_PYTHON}"
              "-DVENV_BIN=${_venv_bin}"
              "-DSRC=${ARG_SOURCE}"
              "-DOUT=${_out}"
              "-DFORMAT=${fmt}"
              "-DDATA_DIR=${_data}"
              -P "${MparkWg21_RENDER_SCRIPT}"
      DEPENDS "${ARG_SOURCE}"
              "${Pandoc_EXECUTABLE}"
              "${_data}/metadata.yaml"
              "${_data}/csl.json" "${_data}/srefs.json" "${_data}/srefs.defs"
      WORKING_DIRECTORY "${_src_dir}"
      COMMENT "Rendering ${name}.${fmt}"
      VERBATIM)
    list(APPEND _outputs "${_out}")
  endforeach()

  if(ARG_ALL)
    add_custom_target(${name} ALL DEPENDS ${_outputs})
  else()
    add_custom_target(${name} DEPENDS ${_outputs})
  endif()
  add_dependencies(${name} wg21_data)
endfunction()
