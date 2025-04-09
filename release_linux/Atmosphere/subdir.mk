################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Atmosphere/read_climate_maps.cpp \
../codes/Atmosphere/read_groundTs_maps.cpp \


OBJS += \
./Atmosphere/read_climate_maps.o \
./Atmosphere/read_groundTs_maps.o \


CPP_DEPS += \
./Atmosphere/read_climate_maps.d \
./Atmosphere/read_groundTs_maps.d \


# Each subdirectory must supply rules for building sources it contributes
Atmosphere/%.o: ../codes/Atmosphere/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
