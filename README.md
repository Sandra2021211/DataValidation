**Data Validation Progress Summary**

**Task 1 – Column Mapping**

**Date:** 10-06-2025

**Highlights:**

            1. Validated column mappings between source and destination files using mapping.json.

            2. Detected unmapped columns through set operations and logged discrepancies.
            
**Summary:** Started building the data validation tool by aligning column names between source and destination files. Extracted column names, compared them, and logged unmapped ones if any. This foundational task set the stage for accurate data validation.

**Task 2 – Data Integrity Checks**

**Date:** 11-06-2025

**Highlights:**

            1. Checked for empty rows and duplicate entries.

            2. Validated data types for mapped columns.
            
            3. Compared row and column counts using df.shape().
            
**Summary:** Enhanced data integrity by removing empty rows, identifying duplicates, and validating data types between source and destination. Structural discrepancies were caught early, ensuring clean data for further validation steps.

**Task 3 – Unique Key Identification**

**Date:** 12-06-2025

**Highlights:**

            1. Found a unique key by combining columns iteratively.

            2. Ensured row-level uniqueness for future validations.
            
**Summary:** Determined a unique identifier for each row by testing single and multi-column combinations. This hands-on process deepened my understanding of the dataset’s structure and prepared it for precise row-level validation.

**Task 4 – Dataset Creation and Validation**

**Date:** 13-06-2025

**Highlights:**

           1. Created a 50x50 dataset with unique rows and columns, ensuring no duplicates.
           
           2. Validated the dataset for any mismatches or inconsistencies.
           
           3. Processed a 10k-row dataset by adding stream time and setting start/end dates.
         
           4. Filtered and analyzed the data to detect any discrepancies.

**Summary:** Built a clean dataset of 50 rows and 50 columns with no duplicates and confirmed its integrity. Additionally, for a 10k-row dataset, stream time and start/end dates were added, followed by filtering to identify any mismatches. These steps ensured both datasets were accurate and ready for further use.

**Task 5 – Customizing with Dates**

**Date:** 16-06-2025

**Highlights:**

         1. Added a date column to source and destination datasets.
         
         2. Implemented custom validation based on a specified date range.
      
         3. Enabled filtering and validation for time-bound data.

**Summary:** Enhanced the validation tool by introducing date-based filtering. The new feature allows the tool to focus on rows within a specific date range, enabling more targeted and context-aware checks. This improvement boosts flexibility and prepares the tool for real-world, time-sensitive use cases.

**Task 6 – Optimizing Performance**

**Date:** 17-06-2025

**Highlights:**

         1. Introduced multithreading to speed up validation tasks.

         2. Logged execution times for each validation step.

**Summary:** Focused on improving performance by implementing multithreading, allowing multiple validations to run concurrently. This optimization drastically reduced processing time for large datasets. Time tracking and logging added transparency, showcasing the efficiency gains. The tool is now not only reliable but also fast.

**Task 7 – Advancing with Multiprocessing**

**Date:** 18-06-2025

**Highlights:**

        1. Replaced multithreading with multiprocessing for CPU-intensive validations.
        
        2. Measured and compared execution times to highlight performance gains.

**Summary:** Built on previous optimizations by implementing multiprocessing for resource-heavy tasks. This approach improved efficiency, reducing validation times significantly. The shift ensures better utilization of system resources, marking another step toward a highly performant and scalable validation tool.

**Task 8 – Threads vs. Processes**

**Date:** 19-06-2025

**Highlights:**

        1. Benchmarked multithreading against multiprocessing for validation tasks.
        
        2. Confirmed multiprocessing's superior performance for CPU-heavy operations.

**Summary:** Conducted a detailed comparison between multithreading and multiprocessing. While threads excelled in I/O-bound tasks, processes outperformed them in CPU-intensive validations, reducing execution time significantly. This analysis validated my architectural decisions and further optimized the tool for diverse workloads.

**Task 9 – Mapping-Free Validation**

**Date:** 20-06-2025

**Highlights:**

        1. Enabled validation without dependency on `mapping.json`.
    
        2.  Introduced column matching through direct value comparison.

**Summary:** Enhanced the tool to operate without predefined mappings by comparing data values directly between source and destination. This innovation adds flexibility, allowing validation even for datasets without structured mappings, making the tool more adaptable to diverse scenarios.

**Task 10 – Advanced Row and Column Matching**

**Date:** 23-06-2025

**Highlights:**

        1. Filtered rows with matching primary keys and aligned them as the index.
        
        2. Compared columns by position and calculated value match percentages.
        
        3. Used value similarity checks for unmatched columns, identifying high-similarity pairs (>80%).
        
        4. Output best-matching column pairs for improved mapping and validation.

**Summary:** Enhanced the tool with precise row alignment and advanced column matching techniques. By combining positional and value-based comparisons, it now identifies highly reliable column pairs, streamlining validation and mapping tasks.

**Task 11 – Ensuring High Match Accuracy**

**Date:** 24-06-2025

**Highlights:**

       1. Built a script to compare source and destination datasets, focusing on missing details.
    
       2. Ensured a minimum 90% match threshold for validation accuracy.
       
       3. Achieved 100% match for integer values.

       4. Implemented logic to handle decimals by converting them to integers (e.g., `57000.67` to `57000`) for seamless comparisons.

**Summary:** The script effectively identifies missing data between datasets while maintaining high accuracy. By handling decimal-to-integer conversions, it ensures precise validation, delivering consistent and reliable results.


