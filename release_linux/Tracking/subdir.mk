################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Tracking/Mixing.cpp \
../codes/Tracking/Mixing_canopy.cpp \
../codes/Tracking/Fractionation.cpp \
../codes/Tracking/Mixing_soil_profile.cpp \
../codes/Tracking/Mixing_snow.cpp \


OBJS += \
./Tracking/Mixing.o \
./Tracking/Mixing_canopy.o \
./Tracking/Fractionation.o \
./Tracking/Mixing_soil_profile.o \
./Tracking/Mixing_snow.o \


CPP_DEPS += \
./Tracking/Mixing.d \
./Tracking/Mixing_canopy.d \
./Tracking/Fractionation.d \
./Tracking/Mixing_soil_profile.d \
./Tracking/Mixing_snow.d \


# Each subdirectory must supply rules for building sources it contributes
Tracking/%.o: ../codes/Tracking/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
