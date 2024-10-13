# Context

Empirical Analysis
Objectives:
Experimentally verify concepts of analysis and asymptotic behavior of the algorithms discussed in theoretical classes, activities and exercises.
Carry out a project and execute an empirical analysis, involving concepts of sampling and statistical tools.
Description:
Perform an Empirical Analysis of the Sorting Algorithms discussed in the course:

Insertion Sort, Selection Sort, Merge Sort, Heap Sort and Quick Sort.

Develop an experimental project considering good practices for an adequate empirical analysis:

Implementation under similar conditions;
Definition of measures (time, number of comparisons/exchanges);
Definition of sampling (interval and variation of sample size);
Analysis of results through several executions, using statistical tools (mean, standard deviation).

Discussion of the results obtained and expected, according to theoretical analysis.
Best/worst case analyses, as well as average case will be considered as an additional.

---

Empirical Analysis of Sorting Algorithms

Objectives

Verify Theoretical Concepts: Experimentally validate concepts of analysis and asymptotic behavior for sorting algorithms discussed during classes.

Project Execution and Empirical Analysis: Develop a project and carry out an empirical analysis, involving concepts of sampling, time measurement, and statistical evaluation.

Description

This empirical analysis aims to compare the efficiency of several sorting algorithms: Insertion Sort, Selection Sort, Merge Sort, Heap Sort, and Quick Sort. The focus will be on measuring the practical behavior of these algorithms in terms of time complexity, number of comparisons, and swaps under various scenarios. Best, average, and worst-case scenarios will be analyzed to confirm or contrast with their theoretical expectations.

Experimental Project and Methodology

The following practices will be employed to ensure a fair and consistent analysis of each sorting algorithm.

1. Implementation under Similar Conditions

To ensure an unbiased comparison:

All algorithms will be implemented in the same programming language (e.g., Python, Java, or C++) and run on the same hardware.

Uniform data structures and I/O routines will be utilized to keep external influences consistent.

Compiler or interpreter optimizations will be consistent across all algorithms.

2. Definition of Measures

The performance of each algorithm will be evaluated using several key metrics:

Execution Time: Measure the actual running time for sorting various datasets.

Number of Comparisons: Count the number of key comparisons made during sorting.

Number of Exchanges: Count the number of data swaps.

These metrics provide a more granular view of each algorithm's performance and allow for cross-algorithm comparison.

3. Definition of Sampling

Sampling is critical to understand the behavior of each sorting algorithm under different conditions:

Input Size Variation: Execute sorting for various input sizes, such as 100, 1,000, 10,000, and 100,000 elements.

Types of Input Data:

Random Data: Data randomly generated to represent an average-case scenario.

Sorted Data: Data already sorted to determine the best or worst-case scenario (depending on the algorithm).

Reverse Sorted Data: A sequence sorted in reverse order, often representing a worst-case scenario for algorithms like Insertion Sort.

The intervals and variations of sample sizes will be decided based on the available hardware's capacity to ensure that meaningful data is collected without overburdening the system.

4. Analysis of Results with Statistical Tools

Each experiment will be repeated several times (e.g., 30 runs) to reduce the effects of outliers and obtain more reliable performance metrics. For each dataset and input size:

Mean and Standard Deviation will be computed to understand central tendencies and variability in execution time, comparisons, and exchanges.

Box Plots will be generated to visualize the distribution of each algorithm's execution time across different input sizes.

Discussion of Results

The discussion will compare the empirical results with the theoretical expectations for each algorithm:

Insertion Sort: Known to have  complexity in the worst case (reverse sorted data) and  complexity in the best case (already sorted data).

Selection Sort: Always performs  comparisons regardless of input but varies in the number of swaps.

Merge Sort: Should demonstrate  complexity consistently across different input types, as it divides the input regardless of its order.

Heap Sort: Expected to show  behavior across all cases, though it may exhibit different constants depending on input characteristics.

Quick Sort: Often  in the average case but  in the worst case when poor pivot choices are made (e.g., sorted data with naive pivot selection).

Best/Worst/Average Cases: The empirical results will be compared for the best, worst, and average cases:

Expected trends will be contrasted with actual performance data.

Outlier behaviors, if present, will be discussed in terms of pivot selection (Quick Sort) or other nuances.

Conclusion

The analysis will conclude by summarizing the key insights derived from the empirical study, highlighting the practical advantages or disadvantages of each sorting algorithm beyond the theoretical analysis.

Scalability: Which algorithms are suitable for very large datasets?

Real-World Utility: Under which conditions would one algorithm be preferable over others?

Statistical Reliability: How consistent are the performances of different sorting algorithms, and how do they align with theoretical predictions?

This conclusion will aim to help in understanding when and why a particular sorting algorithm should be used in practical scenarios.

