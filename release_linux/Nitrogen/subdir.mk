################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../src/Nitrogen/Nitrogen_addition.cpp \
../src/Nitrogen/Nitrogen_instream_transformation.cpp \
../src/Nitrogen/Nitrogen_summary.cpp \
../src/Nitrogen/Plant_uptake.cpp \
../src/Nitrogen/Soil_denitrification.cpp \


OBJS += \
./Nitrogen/Nitrogen_addition.o \
./Nitrogen/Nitrogen_instream_transformation.o \
./Nitrogen/Nitrogen_summary.o \
./Nitrogen/Plant_uptake.o \
./Nitrogen/Soil_denitrification.o \


CPP_DEPS += \
./Nitrogen/Nitrogen_addition.d \
./Nitrogen/Nitrogen_instream_transformation.d \
./Nitrogen/Nitrogen_summary.d \
./Nitrogen/Plant_uptake.d \
./Nitrogen/Soil_denitrification.d \


# Each subdirectory must supply rules for building sources it contributes
Nitrogen/%.o: ../src/Nitrogen/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../src/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
