################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Nitrogen/Solve_GW_nitrogen.cpp \
../codes/Nitrogen/Solve_canopy_nitrogen.cpp \
../codes/Nitrogen/Plant_uptake.cpp \
../codes/Nitrogen/Solve_routing_nitrogen.cpp \
../codes/Nitrogen/Solve_surface_nitrogen.cpp \
../codes/Nitrogen/Instream_transformation.cpp \
../codes/Nitrogen/Nitrogen_addition.cpp \
../codes/Nitrogen/Soil_denitrification.cpp \
../codes/Nitrogen/Soil_transformation.cpp \
../codes/Nitrogen/Solve_channel_nitrogen.cpp \
../codes/Nitrogen/Solve_soil_profile_nitrogen.cpp \


OBJS += \
./Nitrogen/Solve_GW_nitrogen.o \
./Nitrogen/Solve_canopy_nitrogen.o \
./Nitrogen/Plant_uptake.o \
./Nitrogen/Solve_routing_nitrogen.o \
./Nitrogen/Solve_surface_nitrogen.o \
./Nitrogen/Instream_transformation.o \
./Nitrogen/Nitrogen_addition.o \
./Nitrogen/Soil_denitrification.o \
./Nitrogen/Soil_transformation.o \
./Nitrogen/Solve_channel_nitrogen.o \
./Nitrogen/Solve_soil_profile_nitrogen.o \


CPP_DEPS += \
./Nitrogen/Solve_GW_nitrogen.d \
./Nitrogen/Solve_canopy_nitrogen.d \
./Nitrogen/Plant_uptake.d \
./Nitrogen/Solve_routing_nitrogen.d \
./Nitrogen/Solve_surface_nitrogen.d \
./Nitrogen/Instream_transformation.d \
./Nitrogen/Nitrogen_addition.d \
./Nitrogen/Soil_denitrification.d \
./Nitrogen/Soil_transformation.d \
./Nitrogen/Solve_channel_nitrogen.d \
./Nitrogen/Solve_soil_profile_nitrogen.d \


# Each subdirectory must supply rules for building sources it contributes
Nitrogen/%.o: ../codes/Nitrogen/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
