#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "nncase" for configuration "Release"
set_property(TARGET nncase APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nncase PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libnncase.so"
  IMPORTED_SONAME_RELEASE "libnncase.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS nncase )
list(APPEND _IMPORT_CHECK_FILES_FOR_nncase "${_IMPORT_PREFIX}/lib/libnncase.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
