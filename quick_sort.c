/* quick_sort_dat.c */

#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/stat.h>
#include <sys/types.h>

#include "config.h"

typedef struct {
    double execution_time_sec;
    long long comparisons;
    long long exchanges;
} Metrics;

// Function to partition the array
long long partition(long long *arr, long long low, long long high, Metrics *metrics) {
    long long pivot = arr[high];
    long long i = low - 1;

    for (long long j = low; j <= high - 1; j++) {
        metrics->comparisons++;
        if (arr[j] <= pivot) {
            i++;
            // Swap arr[i] and arr[j]
            long long temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
            metrics->exchanges++;
        }
    }
    // Swap arr[i + 1] and arr[high] (pivot)
    long long temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    metrics->exchanges++;

    return i + 1;
}

// QuickSort function
void quick_sort_recursive(long long *arr, long long low, long long high, Metrics *metrics) {
    if (low < high) {
        long long pi = partition(arr, low, high, metrics);

        // Separately sort elements before and after partition
        quick_sort_recursive(arr, low, pi - 1, metrics);
        quick_sort_recursive(arr, pi + 1, high, metrics);
    }
}

void quick_sort(long long *arr, long long n, Metrics *metrics) {
    // Initialize metrics
    metrics->comparisons = 0;
    metrics->exchanges = 0;

    // Start timing
    struct timespec start_time, end_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    // Perform quick sort
    quick_sort_recursive(arr, 0, n - 1, metrics);

    // End timing
    clock_gettime(CLOCK_MONOTONIC, &end_time);

    // Compute execution time in seconds
    metrics->execution_time_sec = (end_time.tv_sec - start_time.tv_sec) +
        (end_time.tv_nsec - start_time.tv_nsec) / 1e9;
}

// Read data from .dat file into an array
long long *read_data_from_dat(const char *filename, long long *size_ptr) {
    FILE *dat_file = fopen(filename, "rb");
    if (dat_file == NULL) {
        perror("fopen");
        exit(EXIT_FAILURE);
    }

    // Read the size of the data array
    long long size;
    fread(&size, sizeof(long long), 1, dat_file);

    // Allocate memory for the data array
    long long *data = malloc(size * sizeof(long long));
    if (data == NULL) {
        fprintf(stderr, "Memory allocation failed for data array.\n");
        fclose(dat_file);
        exit(EXIT_FAILURE);
    }

    // Read data values
    fread(data, sizeof(long long), size, dat_file);

    fclose(dat_file);

    *size_ptr = size;
    return data;
}

// Function to generate sample sizes (using config.h)
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

int main() {
    // Create the "metrics" directory if it doesn't exist
    struct stat st = {0};
    if (stat("metrics", &st) == -1) {
        if (mkdir("metrics", 0700) != 0) {
            perror("mkdir");
            exit(EXIT_FAILURE);
        }
    }

    // Define data types
    const char *data_types[] = {"random", "sorted", "reverse_sorted"};
    const int num_data_types = 3;

    // Generate sample sizes
    int *input_sizes;
    int NUM_SIZES = generate_sample_sizes(&input_sizes);

    // Open a CSV file to write metrics
    FILE *csv_file = fopen("metrics/quick_sort_metrics.csv", "w");
    if (csv_file == NULL) {
        perror("fopen");
        exit(EXIT_FAILURE);
    }

    // Write CSV headers
    fprintf(csv_file, "Size,Data Type,Run,Execution Time (sec),Comparisons,Exchanges\n");

    // Iterate over sizes and data types
    for (int idx = 0; idx < NUM_SIZES; idx++) {
        long long size = input_sizes[idx];
        printf("Processing datasets of size: %lld\n", size);

        for (int dtype = 0; dtype < num_data_types; dtype++) {
            // Build the filename
            char filename[256];
            snprintf(filename, sizeof(filename), "samples/data_size_%lld_type_%s.dat", size, data_types[dtype]);

            // Read data from .dat file
            long long data_size;
            long long *original_data = read_data_from_dat(filename, &data_size);

            // Allocate memory for the working data array
            long long *data = malloc(data_size * sizeof(long long));
            if (data == NULL) {
                fprintf(stderr, "Memory allocation failed for data array.\n");
                free(original_data);
                free(input_sizes);
                fclose(csv_file);
                exit(EXIT_FAILURE);
            }

            // Perform multiple runs
            for (int run = 1; run <= NUM_RUNS; run++) {
                // Copy the original data into the working array
                memcpy(data, original_data, data_size * sizeof(long long));

                // Perform quick sort
                Metrics metrics;
                quick_sort(data, data_size, &metrics);

                // Write metrics to CSV
                fprintf(csv_file, "%lld,%s,%d,%.6f,%lld,%lld\n", data_size, data_types[dtype], run,
                        metrics.execution_time_sec, metrics.comparisons, metrics.exchanges);
            }

            // Free allocated memory
            free(data);
            free(original_data);
        }
        printf("\n");
    }

    fclose(csv_file);

    // Free the input_sizes array
    free(input_sizes);

    printf("Metrics have been exported to metrics/quick_sort_metrics.csv\n");

    return 0;
}
