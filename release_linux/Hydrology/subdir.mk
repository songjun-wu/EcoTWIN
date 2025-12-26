################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../src/Hydrology/Canopy_evaporation.cpp \
../src/Hydrology/Channel_evaporation.cpp \
../src/Hydrology/Check_mass_balance.cpp \
../src/Hydrology/Evapotranspiration.cpp \
../src/Hydrology/GWrecharge.cpp \
../src/Hydrology/Infiltration.cpp \
../src/Hydrology/Initialisation.cpp \
../src/Hydrology/Interception.cpp \
../src/Hydrology/Irrigation.cpp \
../src/Hydrology/Percolation.cpp \
../src/Hydrology/ReGWrecharge.cpp \
../src/Hydrology/Reinfiltration.cpp \
../src/Hydrology/Repercolation.cpp \
../src/Hydrology/Routing_GWflow.cpp \
../src/Hydrology/Routing_Q.cpp \
../src/Hydrology/Routing_interflow.cpp \
../src/Hydrology/Routing_overland_flow.cpp \
../src/Hydrology/Seperate_PET.cpp \
../src/Hydrology/Soil_proporty.cpp \
../src/Hydrology/Store_states.cpp \
../src/Hydrology/Drainage.cpp \
../src/Hydrology/Routing_drainage.cpp \
../src/Hydrology/Hydrology_summary.cpp \


OBJS += \
./Hydrology/Canopy_evaporation.o \
./Hydrology/Channel_evaporation.o \
./Hydrology/Check_mass_balance.o \
./Hydrology/Evapotranspiration.o \
./Hydrology/GWrecharge.o \
./Hydrology/Infiltration.o \
./Hydrology/Initialisation.o \
./Hydrology/Interception.o \
./Hydrology/Irrigation.o \
./Hydrology/Percolation.o \
./Hydrology/ReGWrecharge.o \
./Hydrology/Reinfiltration.o \
./Hydrology/Repercolation.o \
./Hydrology/Routing_GWflow.o \
./Hydrology/Routing_Q.o \
./Hydrology/Routing_interflow.o \
./Hydrology/Routing_overland_flow.o \
./Hydrology/Seperate_PET.o \
./Hydrology/Soil_proporty.o \
./Hydrology/Store_states.o \
./Hydrology/Drainage.o \
./Hydrology/Routing_drainage.o \
./Hydrology/Hydrology_summary.o \


CPP_DEPS += \
./Hydrology/Canopy_evaporation.d \
./Hydrology/Channel_evaporation.d \
./Hydrology/Check_mass_balance.d \
./Hydrology/Evapotranspiration.d \
./Hydrology/GWrecharge.d \
./Hydrology/Infiltration.d \
./Hydrology/Initialisation.d \
./Hydrology/Interception.d \
./Hydrology/Irrigation.d \
./Hydrology/Percolation.d \
./Hydrology/ReGWrecharge.d \
./Hydrology/Reinfiltration.d \
./Hydrology/Repercolation.d \
./Hydrology/Routing_GWflow.d \
./Hydrology/Routing_Q.d \
./Hydrology/Routing_interflow.d \
./Hydrology/Routing_overland_flow.d \
./Hydrology/Seperate_PET.d \
./Hydrology/Soil_proporty.d \
./Hydrology/Store_states.d \
./Hydrology/Drainage.d \
./Hydrology/Routing_drainage.d \
./Hydrology/Hydrology_summary.d \


# Each subdirectory must supply rules for building sources it contributes
Hydrology/%.o: ../src/Hydrology/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../src/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
