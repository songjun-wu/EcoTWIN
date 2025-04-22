################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Functions/Sort_root_fraction.cpp \
../codes/Functions/Sort_datetime.cpp \
../codes/Functions/Sort_percolation_travel_time.cpp \


OBJS += \
./Functions/Sort_root_fraction.o \
./Functions/Sort_datetime.o \
./Functions/Sort_percolation_travel_time.o \


CPP_DEPS += \
./Functions/Sort_root_fraction.d \
./Functions/Sort_datetime.d \
./Functions/Sort_percolation_travel_time.d \


# Each subdirectory must supply rules for building sources it contributes
Functions/%.o: ../codes/Functions/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
