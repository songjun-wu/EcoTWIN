################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../src/Spatial/grid.cpp \
../src/Spatial/parameterisation.cpp \
../src/Spatial/sortGridLDD.cpp \
../src/Spatial/sortTSmask.cpp \


OBJS += \
./Spatial/grid.o \
./Spatial/parameterisation.o \
./Spatial/sortGridLDD.o \
./Spatial/sortTSmask.o \


CPP_DEPS += \
./Spatial/grid.d \
./Spatial/parameterisation.d \
./Spatial/sortGridLDD.d \
./Spatial/sortTSmask.d \


# Each subdirectory must supply rules for building sources it contributes
Spatial/%.o: ../src/Spatial/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../src/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
