cmake_minimum_required(VERSION 3.18)
project(ttt_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(pybind11 REQUIRED)

pybind11_add_module(ttt_cpp cpp/ttt_ai.cpp)
