# FindPandoc -- locate the pandoc executable (it ships no CMake config) and
# probe its version. Sets Pandoc_FOUND / Pandoc_EXECUTABLE / Pandoc_VERSION and
# a GLOBAL imported target Pandoc::pandoc. Hint: Pandoc_ROOT (or a system
# pandoc on PATH).

find_program(Pandoc_EXECUTABLE
  NAMES pandoc
  HINTS ${Pandoc_ROOT} ENV Pandoc_ROOT
  PATH_SUFFIXES bin
  DOC "Path to the pandoc executable")

if(Pandoc_EXECUTABLE)
  execute_process(
    COMMAND "${Pandoc_EXECUTABLE}" --version
    OUTPUT_VARIABLE _pandoc_version_output
    ERROR_QUIET
    OUTPUT_STRIP_TRAILING_WHITESPACE
    RESULT_VARIABLE _pandoc_version_rc)
  if(_pandoc_version_rc EQUAL 0 AND
     _pandoc_version_output MATCHES "pandoc[^0-9]*([0-9]+(\\.[0-9]+)+)")
    set(Pandoc_VERSION "${CMAKE_MATCH_1}")
  endif()
  unset(_pandoc_version_output)
  unset(_pandoc_version_rc)
endif()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Pandoc
  REQUIRED_VARS Pandoc_EXECUTABLE
  VERSION_VAR Pandoc_VERSION)

if(Pandoc_FOUND AND NOT TARGET Pandoc::pandoc)
  add_executable(Pandoc::pandoc IMPORTED GLOBAL)
  set_target_properties(Pandoc::pandoc PROPERTIES
    IMPORTED_LOCATION "${Pandoc_EXECUTABLE}")
endif()

mark_as_advanced(Pandoc_EXECUTABLE)
