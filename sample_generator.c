/* sample_generator.c */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include "config.h"

// Function to generate sample sizes
int generate_sample_sizes(int **sizes_ptr) {
    int *sizes = malloc(MAX_SIZES * sizeof(int));
    if (sizes == NULL) {
        fprintf(stderr, "Memory allocation failed for sample sizes.\n");
        exit(EXIT_FAILURE);
    }

    int count = 0;

    for (int size = START_SIZE; size <= END_SIZE; size += STEP_SIZE) {
        sizes[count++] = size;
    }

    *sizes_ptr = sizes;
    return count;  // Return the number of sizes generated
}

// Function to generate random data
void generate_random_data(long long size, long long *arr) {
    for (long long i = 0; i < size; i++) {
        arr[i] = rand() % (size * 10) + 1;  // Random integers between 1 and size*10
    }
}

// Function to generate sorted data
void generate_sorted_data(long long size, long long *arr) {
    for (long long i = 0; i < size; i++) {
        arr[i] = i + 1;  // Integers from 1 to size
    }
}

// Function to generate reverse sorted data
void generate_reverse_sorted_data(long long size, long long *arr) {
    for (long long i = 0; i < size; i++) {
        arr[i] = size - i;  // Integers from size down to 1
    }
}

int main() {
    // Seed the random number generator
    srand((unsigned int)time(NULL));

    // Define data types
    const char *data_types[] = {"random", "sorted", "reverse_sorted"};
    const int num_data_types = 3;

    // Generate sample sizes
    int *input_sizes;
    int NUM_SIZES = generate_sample_sizes(&input_sizes);

    // Create the "samples" directory if it doesn't exist
    struct stat st = {0};
    if (stat("samples", &st) == -1) {
        if (mkdir("samples", 0700) != 0) {
            perror("mkdir");
            free(input_sizes);
            exit(EXIT_FAILURE);
        }
    }

    // Generate samples and export to .dat files in "samples" directory
    for (int idx = 0; idx < NUM_SIZES; idx++) {
        long long size = input_sizes[idx];
        printf("Generating data samples for size: %lld\n", size);

        // Allocate memory once per size
        long long *data = malloc(size * sizeof(long long));
        if (data == NULL) {
            fprintf(stderr, "Memory allocation failed for data of size %lld.\n", size);
            free(input_sizes);
            exit(EXIT_FAILURE);
        }

        for (int dtype = 0; dtype < num_data_types; dtype++) {
            if (strcmp(data_types[dtype], "random") == 0) {
                generate_random_data(size, data);
            } else if (strcmp(data_types[dtype], "sorted") == 0) {
                generate_sorted_data(size, data);
            } else if (strcmp(data_types[dtype], "reverse_sorted") == 0) {
                generate_reverse_sorted_data(size, data);
            }

            // Create .dat file for this dataset
            char filename[256];
            snprintf(filename, sizeof(filename), "samples/data_size_%lld_type_%s.dat", size, data_types[dtype]);
            FILE *dat_file = fopen(filename, "wb");
            if (dat_file == NULL) {
                perror("fopen");
                free(data);
                free(input_sizes);
                exit(EXIT_FAILURE);
            }

            // Write the size of the data as the first element
            if (fwrite(&size, sizeof(long long), 1, dat_file) != 1) {
                fprintf(stderr, "Error writing size to file %s.\n", filename);
                fclose(dat_file);
                free(data);
                free(input_sizes);
                exit(EXIT_FAILURE);
            }

            // Write data values
            size_t elements_written = fwrite(data, sizeof(long long), size, dat_file);
            if (elements_written != size) {
                fprintf(stderr, "Error writing data to file %s.\n", filename);
                fclose(dat_file);
                free(data);
                free(input_sizes);
                exit(EXIT_FAILURE);
            }

            fclose(dat_file);
        }

        // Free the allocated memory
        free(data);
        printf("\n");
    }

    printf("Data samples have been exported to .dat files in the 'samples' directory.\n");

    // Free the input_sizes array
    free(input_sizes);

    return 0;
}
