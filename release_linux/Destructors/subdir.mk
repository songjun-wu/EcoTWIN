################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Destructors/ControlDestruct.cpp \
../codes/Destructors/AtmosphereDestruct.cpp \
../codes/Destructors/ParamDestruct.cpp \
../codes/Destructors/BasinDestruct.cpp \
../codes/Destructors/ReportDestruct.cpp \


OBJS += \
./Destructors/ControlDestruct.o \
./Destructors/AtmosphereDestruct.o \
./Destructors/ParamDestruct.o \
./Destructors/BasinDestruct.o \
./Destructors/ReportDestruct.o \


CPP_DEPS += \
./Destructors/ControlDestruct.d \
./Destructors/AtmosphereDestruct.d \
./Destructors/ParamDestruct.d \
./Destructors/BasinDestruct.d \
./Destructors/ReportDestruct.d \


# Each subdirectory must supply rules for building sources it contributes
Destructors/%.o: ../codes/Destructors/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
