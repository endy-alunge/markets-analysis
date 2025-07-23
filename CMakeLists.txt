cmake_minimum_required(VERSION 3.16)
project(markets_analysis LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Make sure to pass this toolchain file when running cmake:
# -DCMAKE_TOOLCHAIN_FILE=[vcpkg-root]/scripts/buildsystems/vcpkg.cmake
find_package(cpr CONFIG REQUIRED)

add_executable(markets_analysis main.cpp)
target_link_libraries(markets_analysis PRIVATE cpr::cpr)