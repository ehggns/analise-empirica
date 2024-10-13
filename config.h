/* config.h */

#ifndef CONFIG_H
#define CONFIG_H

// Define the starting size, ending size, and step size
#define START_SIZE 0
#define END_SIZE 100000
#define STEP_SIZE 10000
#define NUM_RUNS 10

// Calculate the maximum number of sample sizes
#define MAX_SIZES (((END_SIZE) - (START_SIZE)) / (STEP_SIZE) + 1)

#endif // CONFIG_H
