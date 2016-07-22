cmake_minimum_required(VERSION 2.8.12)

project(academ-weather)

set(CMAKE_CXX_STANDARD 14)

# ------------ qt

find_package(Qt5 COMPONENTS Core Qml Quick Network)
set(CMAKE_AUTOMOC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

# ------------

aux_source_directory(src SRC_LIST)

set(RESOURCES qml.qrc)

qt5_add_resources(RESOURCES_OBJ ${RESOURCES})

message(STATUS ${CMAKE_MODULE_PATH})

if(ANDROID)
    add_library(${PROJECT_NAME} SHARED ${SRC_LIST} ${RESOURCES_OBJ})
else(ANDROID)
    add_executable(${PROJECT_NAME} ${SRC_LIST} ${RESOURCES_OBJ})
endif(ANDROID)

target_link_libraries(${PROJECT_NAME} Qt5::Quick)

