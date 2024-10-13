#!/bin/bash

# run_all.sh
# A script to automate the execution of sample generation, sorting algorithms, and analysis.

# Exit immediately if a command exits with a non-zero status
set -e

# Function to compile a C program
compile_c_program() {
    local source_file=$1
    local output_file=$2
    echo "Compiling ${source_file}..."
    gcc -O3 -o "${output_file}" "${source_file}"
}

# Function to run a Python script using Poetry
run_python_script() {
    local script_file=$1
    echo "Running ${script_file}..."
    poetry run python "${script_file}"
}

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Please install Poetry before running this script."
    exit 1
fi

echo "Starting the automated process..."

# Step 1: Compile the sample generator
compile_c_program "sample_generator.c" "sample_generator"

# Step 2: Compile the sorting algorithms
compile_c_program "selection_sort.c" "selection_sort"
compile_c_program "insertion_sort.c" "insertion_sort"
compile_c_program "heap_sort.c" "heap_sort"
compile_c_program "merge_sort.c" "merge_sort"
compile_c_program "quick_sort.c" "quick_sort"

# Step 3: Generate samples
echo "Generating samples..."
./sample_generator

# Step 4: Run the sorting algorithms
echo "Running Selection Sort..."
./selection_sort

echo "Running Insertion Sort..."
./insertion_sort

echo "Running Heap Sort..."
./heap_sort

echo "Running Merge Sort..."
./merge_sort

echo "Running Quick Sort..."
./quick_sort

# Step 5: Install Python dependencies using Poetry
echo "Installing Python dependencies..."
poetry install

# Step 6: Run the analysis for each algorithm
echo "Running analysis for each algorithm..."
run_python_script "algorithm_analysis.py"

# Step 7: Run the confrontation scripts
echo "Running confront_sorts.py..."
run_python_script "confront_sorts.py"

echo "Running confront_sorts_log_scale.py..."
run_python_script "confront_sorts_log_scale.py"

echo "All tasks completed successfully. Results are available in the 'analysis' and 'confront_sorts' folders."
