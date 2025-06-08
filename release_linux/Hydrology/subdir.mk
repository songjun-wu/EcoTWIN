################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Hydrology/Check_mass_balance.cpp \
../codes/Hydrology/Percolation.cpp \
../codes/Hydrology/Routing_GWflow.cpp \
../codes/Hydrology/Routing_interflow.cpp \
../codes/Hydrology/Solve_surface.cpp \
../codes/Hydrology/Soil_proporty.cpp \
../codes/Hydrology/Solve_canopy.cpp \
../codes/Hydrology/Solve_soil_profile.cpp \
../codes/Hydrology/Solve_timesteps.cpp \
../codes/Hydrology/Store_states.cpp \
../codes/Hydrology/Canopy_evaporation.cpp \
../codes/Hydrology/Channel_evaporation.cpp \
../codes/Hydrology/GWrecharge.cpp \
../codes/Hydrology/Infiltration.cpp \
../codes/Hydrology/Interception.cpp \
../codes/Hydrology/ReGWrecharge.cpp \
../codes/Hydrology/Routing.cpp \
../codes/Hydrology/Routing_overland_flow.cpp \
../codes/Hydrology/Evapotranspiration.cpp \
../codes/Hydrology/Reinfiltration.cpp \
../codes/Hydrology/Routing_Q.cpp \
../codes/Hydrology/Solve_channel.cpp \
../codes/Hydrology/Irrigation.cpp \
../codes/Hydrology/Initialisation.cpp \
../codes/Hydrology/Repercolation.cpp \
../codes/Hydrology/Seperate_PET.cpp \


OBJS += \
./Hydrology/Check_mass_balance.o \
./Hydrology/Percolation.o \
./Hydrology/Routing_GWflow.o \
./Hydrology/Routing_interflow.o \
./Hydrology/Solve_surface.o \
./Hydrology/Soil_proporty.o \
./Hydrology/Solve_canopy.o \
./Hydrology/Solve_soil_profile.o \
./Hydrology/Solve_timesteps.o \
./Hydrology/Store_states.o \
./Hydrology/Canopy_evaporation.o \
./Hydrology/Channel_evaporation.o \
./Hydrology/GWrecharge.o \
./Hydrology/Infiltration.o \
./Hydrology/Interception.o \
./Hydrology/ReGWrecharge.o \
./Hydrology/Routing.o \
./Hydrology/Routing_overland_flow.o \
./Hydrology/Evapotranspiration.o \
./Hydrology/Reinfiltration.o \
./Hydrology/Routing_Q.o \
./Hydrology/Solve_channel.o \
./Hydrology/Irrigation.o \
./Hydrology/Initialisation.o \
./Hydrology/Repercolation.o \
./Hydrology/Seperate_PET.o \


CPP_DEPS += \
./Hydrology/Check_mass_balance.d \
./Hydrology/Percolation.d \
./Hydrology/Routing_GWflow.d \
./Hydrology/Routing_interflow.d \
./Hydrology/Solve_surface.d \
./Hydrology/Soil_proporty.d \
./Hydrology/Solve_canopy.d \
./Hydrology/Solve_soil_profile.d \
./Hydrology/Solve_timesteps.d \
./Hydrology/Store_states.d \
./Hydrology/Canopy_evaporation.d \
./Hydrology/Channel_evaporation.d \
./Hydrology/GWrecharge.d \
./Hydrology/Infiltration.d \
./Hydrology/Interception.d \
./Hydrology/ReGWrecharge.d \
./Hydrology/Routing.d \
./Hydrology/Routing_overland_flow.d \
./Hydrology/Evapotranspiration.d \
./Hydrology/Reinfiltration.d \
./Hydrology/Routing_Q.d \
./Hydrology/Solve_channel.d \
./Hydrology/Irrigation.d \
./Hydrology/Initialisation.d \
./Hydrology/Repercolation.d \
./Hydrology/Seperate_PET.d \


# Each subdirectory must supply rules for building sources it contributes
Hydrology/%.o: ../codes/Hydrology/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
