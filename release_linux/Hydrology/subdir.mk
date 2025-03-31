################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Hydrology/Evapotranspiration.cpp \
../codes/Hydrology/Solve_timesteps.cpp \
../codes/Hydrology/Infiltration.cpp \
../codes/Hydrology/Percolation.cpp \
../codes/Hydrology/Snow.cpp \
../codes/Hydrology/Soil_proporty.cpp \
../codes/Hydrology/Solve_soil_profile.cpp \
../codes/Hydrology/Solve_canopy.cpp \
../codes/Hydrology/Routing_overland_flow.cpp \
../codes/Hydrology/Routing.cpp \
../codes/Hydrology/Routing_interflow.cpp \
../codes/Hydrology/Routing_Q.cpp \
../codes/Hydrology/Initialisation.cpp \


OBJS += \
./Hydrology/Evapotranspiration.o \
./Hydrology/Solve_timesteps.o \
./Hydrology/Infiltration.o \
./Hydrology/Percolation.o \
./Hydrology/Snow.o \
./Hydrology/Soil_proporty.o \
./Hydrology/Solve_soil_profile.o \
./Hydrology/Solve_canopy.o \
./Hydrology/Routing_overland_flow.o \
./Hydrology/Routing.o \
./Hydrology/Routing_interflow.o \
./Hydrology/Routing_Q.o \
./Hydrology/Initialisation.o \


CPP_DEPS += \
./Hydrology/Evapotranspiration.d \
./Hydrology/Solve_timesteps.d \
./Hydrology/Infiltration.d \
./Hydrology/Percolation.d \
./Hydrology/Snow.d \
./Hydrology/Soil_proporty.d \
./Hydrology/Solve_soil_profile.d \
./Hydrology/Solve_canopy.d \
./Hydrology/Routing_overland_flow.d \
./Hydrology/Routing.d \
./Hydrology/Routing_interflow.d \
./Hydrology/Routing_Q.d \
./Hydrology/Initialisation.d \


# Each subdirectory must supply rules for building sources it contributes
Hydrology/%.o: ../codes/Hydrology/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
