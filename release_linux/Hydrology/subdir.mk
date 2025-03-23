################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Hydrology/Canopy.cpp \
../codes/Hydrology/Snow.cpp \
../codes/Hydrology/Solve_soil_profile.cpp \
../codes/Hydrology/Solve_timesteps.cpp \
../codes/Hydrology/routing_overland_flow.cpp \


OBJS += \
./Hydrology/Canopy.o \
./Hydrology/Snow.o \
./Hydrology/Solve_soil_profile.o \
./Hydrology/Solve_timesteps.o \
./Hydrology/routing_overland_flow.o \


CPP_DEPS += \
./Hydrology/Canopy.d \
./Hydrology/Snow.d \
./Hydrology/Solve_soil_profile.d \
./Hydrology/Solve_timesteps.d \
./Hydrology/routing_overland_flow.d \


# Each subdirectory must supply rules for building sources it contributes
Hydrology/%.o: ../codes/Hydrology/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
