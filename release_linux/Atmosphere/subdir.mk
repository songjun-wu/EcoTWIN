################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../src/Atmosphere/read_climate_maps.cpp \
../src/Atmosphere/read_groundTs_maps.cpp \
../src/Atmosphere/read_managementTs_maps.cpp \


OBJS += \
./Atmosphere/read_climate_maps.o \
./Atmosphere/read_groundTs_maps.o \
./Atmosphere/read_managementTs_maps.o \


CPP_DEPS += \
./Atmosphere/read_climate_maps.d \
./Atmosphere/read_groundTs_maps.d \
./Atmosphere/read_managementTs_maps.d \


# Each subdirectory must supply rules for building sources it contributes
Atmosphere/%.o: ../src/Atmosphere/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../src/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
