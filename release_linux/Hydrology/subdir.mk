################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Hydrology/Canopy_evaporation.cpp \
../codes/Hydrology/Percolation.cpp \
../codes/Hydrology/Repercolation.cpp \
../codes/Hydrology/Routing_GWflow.cpp \
../codes/Hydrology/Seperate_PET.cpp \
../codes/Hydrology/Solve_canopy.cpp \
../codes/Hydrology/Solve_timesteps.cpp \
../codes/Hydrology/Check_mass_balance.cpp \
../codes/Hydrology/ReGWrecharge.cpp \
../codes/Hydrology/GWrecharge.cpp \
../codes/Hydrology/Infiltration.cpp \
../codes/Hydrology/Initialisation.cpp \
../codes/Hydrology/Interception.cpp \
../codes/Hydrology/Routing_Q.cpp \
../codes/Hydrology/Routing_interflow.cpp \
../codes/Hydrology/Soil_proporty.cpp \
../codes/Hydrology/Evapotranspiration.cpp \
../codes/Hydrology/Reinfiltration.cpp \
../codes/Hydrology/Routing.cpp \
../codes/Hydrology/Routing_overland_flow.cpp \
../codes/Hydrology/Solve_soil_profile.cpp \
../codes/Hydrology/Store_states.cpp \
../codes/Hydrology/Solve_surface.cpp \


OBJS += \
./Hydrology/Canopy_evaporation.o \
./Hydrology/Percolation.o \
./Hydrology/Repercolation.o \
./Hydrology/Routing_GWflow.o \
./Hydrology/Seperate_PET.o \
./Hydrology/Solve_canopy.o \
./Hydrology/Solve_timesteps.o \
./Hydrology/Check_mass_balance.o \
./Hydrology/ReGWrecharge.o \
./Hydrology/GWrecharge.o \
./Hydrology/Infiltration.o \
./Hydrology/Initialisation.o \
./Hydrology/Interception.o \
./Hydrology/Routing_Q.o \
./Hydrology/Routing_interflow.o \
./Hydrology/Soil_proporty.o \
./Hydrology/Evapotranspiration.o \
./Hydrology/Reinfiltration.o \
./Hydrology/Routing.o \
./Hydrology/Routing_overland_flow.o \
./Hydrology/Solve_soil_profile.o \
./Hydrology/Store_states.o \
./Hydrology/Solve_surface.o \


CPP_DEPS += \
./Hydrology/Canopy_evaporation.d \
./Hydrology/Percolation.d \
./Hydrology/Repercolation.d \
./Hydrology/Routing_GWflow.d \
./Hydrology/Seperate_PET.d \
./Hydrology/Solve_canopy.d \
./Hydrology/Solve_timesteps.d \
./Hydrology/Check_mass_balance.d \
./Hydrology/ReGWrecharge.d \
./Hydrology/GWrecharge.d \
./Hydrology/Infiltration.d \
./Hydrology/Initialisation.d \
./Hydrology/Interception.d \
./Hydrology/Routing_Q.d \
./Hydrology/Routing_interflow.d \
./Hydrology/Soil_proporty.d \
./Hydrology/Evapotranspiration.d \
./Hydrology/Reinfiltration.d \
./Hydrology/Routing.d \
./Hydrology/Routing_overland_flow.d \
./Hydrology/Solve_soil_profile.d \
./Hydrology/Store_states.d \
./Hydrology/Solve_surface.d \


# Each subdirectory must supply rules for building sources it contributes
Hydrology/%.o: ../codes/Hydrology/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
