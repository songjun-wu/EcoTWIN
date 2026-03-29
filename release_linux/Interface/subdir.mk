################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../src/Interface/Solve_GW_nutrient.cpp \
../src/Interface/Solve_canopy.cpp \
../src/Interface/Solve_canopy_nutrient.cpp \
../src/Interface/Solve_channel.cpp \
../src/Interface/Solve_channel_nutrient.cpp \
../src/Interface/Solve_routing.cpp \
../src/Interface/Solve_routing_nutrient.cpp \
../src/Interface/Solve_soil_profile.cpp \
../src/Interface/Solve_soil_profile_nutrient.cpp \
../src/Interface/Solve_surface.cpp \
../src/Interface/Solve_surface_nutrient.cpp \
../src/Interface/Solve_timesteps.cpp \
../src/Interface/Statistic_summary.cpp \


OBJS += \
./Interface/Solve_GW_nutrient.o \
./Interface/Solve_canopy.o \
./Interface/Solve_canopy_nutrient.o \
./Interface/Solve_channel.o \
./Interface/Solve_channel_nutrient.o \
./Interface/Solve_routing.o \
./Interface/Solve_routing_nutrient.o \
./Interface/Solve_soil_profile.o \
./Interface/Solve_soil_profile_nutrient.o \
./Interface/Solve_surface.o \
./Interface/Solve_surface_nutrient.o \
./Interface/Solve_timesteps.o \
./Interface/Statistic_summary.o \


CPP_DEPS += \
./Interface/Solve_GW_nutrient.d \
./Interface/Solve_canopy.d \
./Interface/Solve_canopy_nutrient.d \
./Interface/Solve_channel.d \
./Interface/Solve_channel_nutrient.d \
./Interface/Solve_routing.d \
./Interface/Solve_routing_nutrient.d \
./Interface/Solve_soil_profile.d \
./Interface/Solve_soil_profile_nutrient.d \
./Interface/Solve_surface.d \
./Interface/Solve_surface_nutrient.d \
./Interface/Solve_timesteps.d \
./Interface/Statistic_summary.d \


# Each subdirectory must supply rules for building sources it contributes
Interface/%.o: ../src/Interface/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../src/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
