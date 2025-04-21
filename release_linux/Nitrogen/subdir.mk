################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Nitrogen/Solve_canopy_nitrogen.cpp \
../codes/Nitrogen/Solve_surface_nitrogen.cpp \
../codes/Nitrogen/Solve_soil_profile_nitrogen.cpp \
../codes/Nitrogen/Solve_GW_nitrogen.cpp \
../codes/Nitrogen/Solve_routing_nitrogen.cpp \
../codes/Nitrogen/Soil_denitrification.cpp \
../codes/Nitrogen/Soil_transformation.cpp \


OBJS += \
./Nitrogen/Solve_canopy_nitrogen.o \
./Nitrogen/Solve_surface_nitrogen.o \
./Nitrogen/Solve_soil_profile_nitrogen.o \
./Nitrogen/Solve_GW_nitrogen.o \
./Nitrogen/Solve_routing_nitrogen.o \
./Nitrogen/Soil_denitrification.o \
./Nitrogen/Soil_transformation.o \


CPP_DEPS += \
./Nitrogen/Solve_canopy_nitrogen.d \
./Nitrogen/Solve_surface_nitrogen.d \
./Nitrogen/Solve_soil_profile_nitrogen.d \
./Nitrogen/Solve_GW_nitrogen.d \
./Nitrogen/Solve_routing_nitrogen.d \
./Nitrogen/Soil_denitrification.d \
./Nitrogen/Soil_transformation.d \


# Each subdirectory must supply rules for building sources it contributes
Nitrogen/%.o: ../codes/Nitrogen/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
