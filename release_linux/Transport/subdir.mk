################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../src/Transport/Solve_soil_transport.cpp \
../src/Transport/Solve_surface_transport.cpp \
../src/Transport/Solve_canopy_transport.cpp \
../src/Transport/Solve_routing_transport.cpp \


OBJS += \
./Transport/Solve_soil_transport.o \
./Transport/Solve_surface_transport.o \
./Transport/Solve_canopy_transport.o \
./Transport/Solve_routing_transport.o \


CPP_DEPS += \
./Transport/Solve_soil_transport.d \
./Transport/Solve_surface_transport.d \
./Transport/Solve_canopy_transport.d \
./Transport/Solve_routing_transport.d \


# Each subdirectory must supply rules for building sources it contributes
Transport/%.o: ../src/Transport/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../src/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
