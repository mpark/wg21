# MPark.WG21
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
#
# Config-mode entry point, so `cmake --install` + CMAKE_PREFIX_PATH works with
# no CMAKE_MODULE_PATH setup. Delegates to the find module, which does the
# real discovery and defines the build API. Works from both the install
# layout (share/cmake/MparkWg21/, with the module under
# share/mpark-wg21/cmake/) and a source checkout (side by side in cmake/).

foreach(_mparkwg21_dir
    "${CMAKE_CURRENT_LIST_DIR}"
    "${CMAKE_CURRENT_LIST_DIR}/../../mpark-wg21/cmake")
  if(EXISTS "${_mparkwg21_dir}/FindMparkWg21.cmake")
    include("${_mparkwg21_dir}/FindMparkWg21.cmake")
    break()
  endif()
endforeach()

if(NOT MparkWg21_FOUND)
  set(MparkWg21_NOT_FOUND_MESSAGE "${_MparkWg21_reason}")
endif()
