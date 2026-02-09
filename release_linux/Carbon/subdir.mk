################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables
CPP_SRCS += \
../src/Carbon/Solve_soil_profile_carbon.cpp \
../src/Carbon/Carbon_transformation.cpp \
../src/Carbon/Carbon_constant.cpp \
../src/Carbon/Assimilation.cpp \
../src/Carbon/Carbon_summary.cpp \
../src/Carbon/Carbon_addition.cpp \
../src/Carbon/Carbon_instream_transformation.cpp \


OBJS += \
./Carbon/Solve_soil_profile_carbon.o \
./Carbon/Carbon_transformation.o \
./Carbon/Carbon_constant.o \
./Carbon/Assimilation.o \
./Carbon/Carbon_summary.o \
./Carbon/Carbon_addition.o \
./Carbon/Carbon_instream_transformation.o \


CPP_DEPS += \
./Carbon/Solve_soil_profile_carbon.d \
./Carbon/Carbon_transformation.d \
./Carbon/Carbon_constant.d \
./Carbon/Assimilation.d \
./Carbon/Carbon_summary.d \
./Carbon/Carbon_addition.d \
./Carbon/Carbon_instream_transformation.d \


# Each subdirectory must supply rules for building sources it contributes
Carbon/%.o: ../src/Carbon/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -ggdb -DCPU_LITTLE_ENDIAN -I"../src/includes" -O3 -ggdb -Wall -c -fmessage-length=0 -fopenmp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '
