################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Destructors/AtmosphereDestruct.cpp \
../codes/Destructors/ControlDestruct.cpp \
../codes/Destructors/BasinDestruct.cpp \
../codes/Destructors/ParamDestruct.cpp \
../codes/Destructors/ReportDestruct.cpp \


OBJS += \
./Destructors/AtmosphereDestruct.o \
./Destructors/ControlDestruct.o \
./Destructors/BasinDestruct.o \
./Destructors/ParamDestruct.o \
./Destructors/ReportDestruct.o \


CPP_DEPS += \
./Destructors/AtmosphereDestruct.d \
./Destructors/ControlDestruct.d \
./Destructors/BasinDestruct.d \
./Destructors/ParamDestruct.d \
./Destructors/ReportDestruct.d \


# Each subdirectory must supply rules for building sources it contributes
Destructors/%.o: ../codes/Destructors/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
