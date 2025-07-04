################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Spatial/grid.cpp \
../codes/Spatial/sortTSmask.cpp \
../codes/Spatial/parameterisation.cpp \
../codes/Spatial/sortGridLDD.cpp \


OBJS += \
./Spatial/grid.o \
./Spatial/sortTSmask.o \
./Spatial/parameterisation.o \
./Spatial/sortGridLDD.o \


CPP_DEPS += \
./Spatial/grid.d \
./Spatial/sortTSmask.d \
./Spatial/parameterisation.d \
./Spatial/sortGridLDD.d \


# Each subdirectory must supply rules for building sources it contributes
Spatial/%.o: ../codes/Spatial/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
