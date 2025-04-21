################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Tracking/Mixing.cpp \
../codes/Tracking/Fractionation.cpp \
../codes/Tracking/Mixing_GW_tracking.cpp \
../codes/Tracking/Mixing_canopy_tracking.cpp \
../codes/Tracking/Mixing_routing_tracking.cpp \
../codes/Tracking/Mixing_soil_profile_tracking.cpp \
../codes/Tracking/Mixing_surface_tracking.cpp \


OBJS += \
./Tracking/Mixing.o \
./Tracking/Fractionation.o \
./Tracking/Mixing_GW_tracking.o \
./Tracking/Mixing_canopy_tracking.o \
./Tracking/Mixing_routing_tracking.o \
./Tracking/Mixing_soil_profile_tracking.o \
./Tracking/Mixing_surface_tracking.o \


CPP_DEPS += \
./Tracking/Mixing.d \
./Tracking/Fractionation.d \
./Tracking/Mixing_GW_tracking.d \
./Tracking/Mixing_canopy_tracking.d \
./Tracking/Mixing_routing_tracking.d \
./Tracking/Mixing_soil_profile_tracking.d \
./Tracking/Mixing_surface_tracking.d \


# Each subdirectory must supply rules for building sources it contributes
Tracking/%.o: ../codes/Tracking/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
