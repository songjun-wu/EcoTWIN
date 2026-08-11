################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../src/Functions/Initialisation.cpp \
../src/Functions/Initialisation_each_timestep.cpp \
../src/Functions/Sort_crop_management.cpp \
../src/Functions/Sort_datetime.cpp \
../src/Functions/Sort_percolation_travel_time.cpp \
../src/Functions/Sort_root_fraction.cpp \
../src/Functions/Sort_soil_transformation_factors.cpp \


OBJS += \
./Functions/Initialisation.o \
./Functions/Initialisation_each_timestep.o \
./Functions/Sort_crop_management.o \
./Functions/Sort_datetime.o \
./Functions/Sort_percolation_travel_time.o \
./Functions/Sort_root_fraction.o \
./Functions/Sort_soil_transformation_factors.o \


CPP_DEPS += \
./Functions/Initialisation.d \
./Functions/Initialisation_each_timestep.d \
./Functions/Sort_crop_management.d \
./Functions/Sort_datetime.d \
./Functions/Sort_percolation_travel_time.d \
./Functions/Sort_root_fraction.d \
./Functions/Sort_soil_transformation_factors.d \


# Each subdirectory must supply rules for building sources it contributes
Functions/%.o: ../src/Functions/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../src/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
