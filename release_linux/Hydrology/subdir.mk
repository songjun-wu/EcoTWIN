################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Hydrology/Evapotranspiration.cpp \
../codes/Hydrology/Snow.cpp \
../codes/Hydrology/Soil_proporty.cpp \
../codes/Hydrology/Infiltration.cpp \
../codes/Hydrology/Initialisation.cpp \
../codes/Hydrology/Percolation.cpp \
../codes/Hydrology/Routing.cpp \
../codes/Hydrology/Routing_Q.cpp \
../codes/Hydrology/Routing_interflow.cpp \
../codes/Hydrology/Routing_overland_flow.cpp \
../codes/Hydrology/Solve_canopy.cpp \
../codes/Hydrology/Solve_soil_profile.cpp \
../codes/Hydrology/Solve_timesteps.cpp \
../codes/Hydrology/Reinfiltration.cpp \
../codes/Hydrology/Repercolation.cpp \
../codes/Hydrology/Interception.cpp \
../codes/Hydrology/Canopy_evaporation.cpp \
../codes/Hydrology/Routing_GWflow.cpp \
../codes/Hydrology/GWrecharge.cpp \
../codes/Hydrology/Store_states.cpp \
../codes/Hydrology/Seperate_PET.cpp \


OBJS += \
./Hydrology/Evapotranspiration.o \
./Hydrology/Snow.o \
./Hydrology/Soil_proporty.o \
./Hydrology/Infiltration.o \
./Hydrology/Initialisation.o \
./Hydrology/Percolation.o \
./Hydrology/Routing.o \
./Hydrology/Routing_Q.o \
./Hydrology/Routing_interflow.o \
./Hydrology/Routing_overland_flow.o \
./Hydrology/Solve_canopy.o \
./Hydrology/Solve_soil_profile.o \
./Hydrology/Solve_timesteps.o \
./Hydrology/Reinfiltration.o \
./Hydrology/Repercolation.o \
./Hydrology/Interception.o \
./Hydrology/Canopy_evaporation.o \
./Hydrology/Routing_GWflow.o \
./Hydrology/GWrecharge.o \
./Hydrology/Store_states.o \
./Hydrology/Seperate_PET.o \


CPP_DEPS += \
./Hydrology/Evapotranspiration.d \
./Hydrology/Snow.d \
./Hydrology/Soil_proporty.d \
./Hydrology/Infiltration.d \
./Hydrology/Initialisation.d \
./Hydrology/Percolation.d \
./Hydrology/Routing.d \
./Hydrology/Routing_Q.d \
./Hydrology/Routing_interflow.d \
./Hydrology/Routing_overland_flow.d \
./Hydrology/Solve_canopy.d \
./Hydrology/Solve_soil_profile.d \
./Hydrology/Solve_timesteps.d \
./Hydrology/Reinfiltration.d \
./Hydrology/Repercolation.d \
./Hydrology/Interception.d \
./Hydrology/Canopy_evaporation.d \
./Hydrology/Routing_GWflow.d \
./Hydrology/GWrecharge.d \
./Hydrology/Store_states.d \
./Hydrology/Seperate_PET.d \


# Each subdirectory must supply rules for building sources it contributes
Hydrology/%.o: ../codes/Hydrology/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
