################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Hydrology/Canopy_evaporation.cpp \
../codes/Hydrology/Repercolation.cpp \
../codes/Hydrology/Routing.cpp \
../codes/Hydrology/Routing_interflow.cpp \
../codes/Hydrology/Solve_surface.cpp \
../codes/Hydrology/Infiltration.cpp \
../codes/Hydrology/Routing_Q.cpp \
../codes/Hydrology/Solve_timesteps.cpp \
../codes/Hydrology/Channel_evaporation.cpp \
../codes/Hydrology/Check_mass_balance.cpp \
../codes/Hydrology/Evapotranspiration.cpp \
../codes/Hydrology/Interception.cpp \
../codes/Hydrology/Percolation.cpp \
../codes/Hydrology/Reinfiltration.cpp \
../codes/Hydrology/Routing_overland_flow.cpp \
../codes/Hydrology/Seperate_PET.cpp \
../codes/Hydrology/Solve_canopy.cpp \
../codes/Hydrology/Solve_soil_profile.cpp \
../codes/Hydrology/Initialisation.cpp \
../codes/Hydrology/Soil_proporty.cpp \
../codes/Hydrology/GWrecharge.cpp \
../codes/Hydrology/Irrigation.cpp \
../codes/Hydrology/ReGWrecharge.cpp \
../codes/Hydrology/Solve_channel.cpp \
../codes/Hydrology/Store_states.cpp \
../codes/Hydrology/Routing_GWflow.cpp \


OBJS += \
./Hydrology/Canopy_evaporation.o \
./Hydrology/Repercolation.o \
./Hydrology/Routing.o \
./Hydrology/Routing_interflow.o \
./Hydrology/Solve_surface.o \
./Hydrology/Infiltration.o \
./Hydrology/Routing_Q.o \
./Hydrology/Solve_timesteps.o \
./Hydrology/Channel_evaporation.o \
./Hydrology/Check_mass_balance.o \
./Hydrology/Evapotranspiration.o \
./Hydrology/Interception.o \
./Hydrology/Percolation.o \
./Hydrology/Reinfiltration.o \
./Hydrology/Routing_overland_flow.o \
./Hydrology/Seperate_PET.o \
./Hydrology/Solve_canopy.o \
./Hydrology/Solve_soil_profile.o \
./Hydrology/Initialisation.o \
./Hydrology/Soil_proporty.o \
./Hydrology/GWrecharge.o \
./Hydrology/Irrigation.o \
./Hydrology/ReGWrecharge.o \
./Hydrology/Solve_channel.o \
./Hydrology/Store_states.o \
./Hydrology/Routing_GWflow.o \


CPP_DEPS += \
./Hydrology/Canopy_evaporation.d \
./Hydrology/Repercolation.d \
./Hydrology/Routing.d \
./Hydrology/Routing_interflow.d \
./Hydrology/Solve_surface.d \
./Hydrology/Infiltration.d \
./Hydrology/Routing_Q.d \
./Hydrology/Solve_timesteps.d \
./Hydrology/Channel_evaporation.d \
./Hydrology/Check_mass_balance.d \
./Hydrology/Evapotranspiration.d \
./Hydrology/Interception.d \
./Hydrology/Percolation.d \
./Hydrology/Reinfiltration.d \
./Hydrology/Routing_overland_flow.d \
./Hydrology/Seperate_PET.d \
./Hydrology/Solve_canopy.d \
./Hydrology/Solve_soil_profile.d \
./Hydrology/Initialisation.d \
./Hydrology/Soil_proporty.d \
./Hydrology/GWrecharge.d \
./Hydrology/Irrigation.d \
./Hydrology/ReGWrecharge.d \
./Hydrology/Solve_channel.d \
./Hydrology/Store_states.d \
./Hydrology/Routing_GWflow.d \


# Each subdirectory must supply rules for building sources it contributes
Hydrology/%.o: ../codes/Hydrology/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
