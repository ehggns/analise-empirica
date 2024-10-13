/* merge_sort_dat.c */

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

// Merge two subarrays of arr[]
void merge(long long *arr, long long l, long long m, long long r, Metrics *metrics) {
    long long n1 = m - l + 1;
    long long n2 = r - m;

    // Create temp arrays
    long long *L = malloc(n1 * sizeof(long long));
    long long *R = malloc(n2 * sizeof(long long));
    if (L == NULL || R == NULL) {
        fprintf(stderr, "Memory allocation failed for temporary arrays in merge.\n");
        exit(EXIT_FAILURE);
    }

    // Copy data to temp arrays L[] and R[]
    memcpy(L, arr + l, n1 * sizeof(long long));
    memcpy(R, arr + m + 1, n2 * sizeof(long long));

    // Merge the temp arrays back into arr[l..r]
    long long i = 0, j = 0, k = l;

    while (i < n1 && j < n2) {
        metrics->comparisons++;
        if (L[i] <= R[j]) {
            arr[k++] = L[i++];
            metrics->exchanges++;
        } else {
            arr[k++] = R[j++];
            metrics->exchanges++;
        }
    }

    // Copy the remaining elements of L[], if any
    while (i < n1) {
        arr[k++] = L[i++];
        metrics->exchanges++;
    }

    // Copy the remaining elements of R[], if any
    while (j < n2) {
        arr[k++] = R[j++];
        metrics->exchanges++;
    }

    // Free temporary arrays
    free(L);
    free(R);
}

// l is for left index and r is right index of the sub-array of arr to be sorted
void merge_sort_recursive(long long *arr, long long l, long long r, Metrics *metrics) {
    if (l < r) {
        long long m = l + (r - l) / 2;

        // Sort first and second halves
        merge_sort_recursive(arr, l, m, metrics);
        merge_sort_recursive(arr, m + 1, r, metrics);

        merge(arr, l, m, r, metrics);
    }
}

void merge_sort(long long *arr, long long n, Metrics *metrics) {
    // Initialize metrics
    metrics->comparisons = 0;
    metrics->exchanges = 0;

    // Start timing
    struct timespec start_time, end_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    // Perform merge sort
    merge_sort_recursive(arr, 0, n - 1, metrics);

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
    FILE *csv_file = fopen("metrics/merge_sort_metrics.csv", "w");
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

                // Perform merge sort
                Metrics metrics;
                merge_sort(data, data_size, &metrics);

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

    printf("Metrics have been exported to metrics/merge_sort_metrics.csv\n");

    return 0;
}
