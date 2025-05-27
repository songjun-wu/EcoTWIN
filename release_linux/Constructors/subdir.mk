################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/Constructors/BasinConstruct.cpp \
../codes/Constructors/ControlConstruct.cpp \
../codes/Constructors/ReportConstruct.cpp \
../codes/Constructors/AtmosphereConstruct.cpp \
../codes/Constructors/ParamConstruct.cpp \


OBJS += \
./Constructors/BasinConstruct.o \
./Constructors/ControlConstruct.o \
./Constructors/ReportConstruct.o \
./Constructors/AtmosphereConstruct.o \
./Constructors/ParamConstruct.o \


CPP_DEPS += \
./Constructors/BasinConstruct.d \
./Constructors/ControlConstruct.d \
./Constructors/ReportConstruct.d \
./Constructors/AtmosphereConstruct.d \
./Constructors/ParamConstruct.d \


# Each subdirectory must supply rules for building sources it contributes
Constructors/%.o: ../codes/Constructors/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
