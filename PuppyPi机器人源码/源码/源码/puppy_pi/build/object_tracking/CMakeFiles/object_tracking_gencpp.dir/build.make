# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.18

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/pi/puppy_pi/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pi/puppy_pi/build

# Utility rule file for object_tracking_gencpp.

# Include the progress variables for this target.
include object_tracking/CMakeFiles/object_tracking_gencpp.dir/progress.make

object_tracking_gencpp: object_tracking/CMakeFiles/object_tracking_gencpp.dir/build.make

.PHONY : object_tracking_gencpp

# Rule to build all files generated by this target.
object_tracking/CMakeFiles/object_tracking_gencpp.dir/build: object_tracking_gencpp

.PHONY : object_tracking/CMakeFiles/object_tracking_gencpp.dir/build

object_tracking/CMakeFiles/object_tracking_gencpp.dir/clean:
	cd /home/pi/puppy_pi/build/object_tracking && $(CMAKE_COMMAND) -P CMakeFiles/object_tracking_gencpp.dir/cmake_clean.cmake
.PHONY : object_tracking/CMakeFiles/object_tracking_gencpp.dir/clean

object_tracking/CMakeFiles/object_tracking_gencpp.dir/depend:
	cd /home/pi/puppy_pi/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pi/puppy_pi/src /home/pi/puppy_pi/src/object_tracking /home/pi/puppy_pi/build /home/pi/puppy_pi/build/object_tracking /home/pi/puppy_pi/build/object_tracking/CMakeFiles/object_tracking_gencpp.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : object_tracking/CMakeFiles/object_tracking_gencpp.dir/depend

