################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Tracking/Fractionation.cpp \
../codes/Tracking/Mixing.cpp \
../codes/Tracking/Mixing_canopy.cpp \
../codes/Tracking/Mixing_snow.cpp \
../codes/Tracking/Mixing_soil_profile.cpp \


OBJS += \
./Tracking/Fractionation.o \
./Tracking/Mixing.o \
./Tracking/Mixing_canopy.o \
./Tracking/Mixing_snow.o \
./Tracking/Mixing_soil_profile.o \


CPP_DEPS += \
./Tracking/Fractionation.d \
./Tracking/Mixing.d \
./Tracking/Mixing_canopy.d \
./Tracking/Mixing_snow.d \
./Tracking/Mixing_soil_profile.d \


# Each subdirectory must supply rules for building sources it contributes
Tracking/%.o: ../codes/Tracking/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
