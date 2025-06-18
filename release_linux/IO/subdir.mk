################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../codes/IO/IO_function.cpp \
../codes/IO/readCropFile.cpp \
../codes/IO/report_for_cali.cpp \
../codes/IO/readConfigFile.cpp \
../codes/IO/readParamFile.cpp \
../codes/IO/report.cpp \


OBJS += \
./IO/IO_function.o \
./IO/readCropFile.o \
./IO/report_for_cali.o \
./IO/readConfigFile.o \
./IO/readParamFile.o \
./IO/report.o \


CPP_DEPS += \
./IO/IO_function.d \
./IO/readCropFile.d \
./IO/report_for_cali.d \
./IO/readConfigFile.d \
./IO/readParamFile.d \
./IO/report.d \


# Each subdirectory must supply rules for building sources it contributes
IO/%.o: ../codes/IO/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../codes/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
