# MPark.WG21
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
#
# This CMake framework for mpark/wg21 provides the function wg21_add_paper
# (see cmake/MparkWg21Helpers.cmake).
#
# This top-level file either configures installation of mpark/wg21 for
# consumption using find_package(MparkWg21) or configures the project to be
# consumed via add_subdirectory().

cmake_minimum_required(VERSION 3.21)

project(MparkWg21
  VERSION 0.1.0
  DESCRIPTION "Pandoc-based framework for authoring and reviewing WG21 papers"
  HOMEPAGE_URL "https://github.com/mpark/wg21"
  LANGUAGES NONE)

if(PROJECT_IS_TOP_LEVEL)
  include(GNUInstallDirs)

  install(DIRECTORY data/
          DESTINATION "${CMAKE_INSTALL_DATADIR}/mpark-wg21/data"
          USE_SOURCE_PERMISSIONS) # pandoc runs the filters via their shebang;
                                  # keep them executable
  install(FILES
            cmake/FindMparkWg21.cmake
            cmake/MparkWg21Helpers.cmake
            cmake/FindPandoc.cmake
            cmake/render.cmake
          DESTINATION "${CMAKE_INSTALL_DATADIR}/mpark-wg21/cmake")

  include(CMakePackageConfigHelpers)
  write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/MparkWg21ConfigVersion.cmake"
    COMPATIBILITY AnyNewerVersion
    ARCH_INDEPENDENT)
  install(FILES
            cmake/MparkWg21Config.cmake
            "${CMAKE_CURRENT_BINARY_DIR}/MparkWg21ConfigVersion.cmake"
          DESTINATION "${CMAKE_INSTALL_DATADIR}/cmake/MparkWg21")
else()
  set(MparkWg21_DATA_SRC      "${CMAKE_CURRENT_SOURCE_DIR}/data")
  set(MparkWg21_RENDER_SCRIPT "${CMAKE_CURRENT_SOURCE_DIR}/cmake/render.cmake")
  include("${CMAKE_CURRENT_SOURCE_DIR}/cmake/MparkWg21Helpers.cmake")
endif()
