################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Control/IO_function.cpp \
../codes/Control/readConfigFile.cpp \
../codes/Control/report.cpp \


OBJS += \
./Control/IO_function.o \
./Control/readConfigFile.o \
./Control/report.o \


CPP_DEPS += \
./Control/IO_function.d \
./Control/readConfigFile.d \
./Control/report.d \


# Each subdirectory must supply rules for building sources it contributes
Control/%.o: ../codes/Control/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
