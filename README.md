**Day 1 – Mapping the COlumn names**
Date: 2025-06-10
Tasks Completed:

Set up initial validation for column mapping between source and destination files.

Used mapping.json to compare expected column mappings.

Implemented logic to detect unmapped columns.

Story:
Today marked the first step in building my data validation tool. The goal was simple: ensure that the columns in the destination file align with those in the source file, using a provided mapping.json. I began by extracting all the column names from both the source and destination files and stored them as sets. Using set operations, I calculated the difference — essentially the columns in the destination file that weren't mapped properly. If any unmapped columns existed, I logged them; otherwise, I confirmed that all columns were correctly mapped. It felt like a small but essential victory — laying the groundwork for all validations to come.

**Day 2 – Laying the Groundwork for Clean Data**
Date: 2025-06-11
Tasks Completed:

Implemented checks for completely empty rows.

Added logic to detect duplicate rows.

Validated data types between source and destination using mapping.json.

Compared row and column counts between source and destination files.

Story:
Building on yesterday’s foundation, today was all about ensuring data integrity. I started with a simple check for fully empty rows using `df.isnull().all(axis=1)`, followed by identifying duplicate entries with `df.duplicated()`. The highlight, though, was data type validation — for each mapped column, I verified that source and destination data types matched. Any mismatches were clearly logged with column names and types. Finally, I compared the row and column counts using `df.shape()` to spot structural discrepancies early. These basic validations might seem small, but they’re the silent guardians of clean, consistent data.

**Day 3 – Finding the Unique Key**
Date: 2025-06-12
Tasks Completed:

Identified a unique key in the dataset through manual combination of columns.

Checked uniqueness progressively: starting with a single column, then combining multiple columns if needed.

Story:
Today was a puzzle-solving session focused on finding a unique key to identify each row. I began by checking if any single column could serve the purpose — no luck. Then, I iteratively combined columns: first two, then three, evaluating their combined uniqueness at each step. This trial-and-error approach finally helped surface a reliable key. Though a bit manual, this method gave me a deeper understanding of the data’s structure. Establishing a unique identifier is a crucial step for future row-level validations.

**Day 4 – Automating Uniqueness**
Date: 2025-06-13
Tasks Completed:

Automated the process of finding a unique key in the dataset.

Programmatically generated combinations of columns to check for uniqueness.

Story:
After manually identifying unique keys yesterday, I decided to streamline the process. I wrote a script to automatically generate all possible combinations of columns and check which set forms a unique key. This significantly reduced manual effort and ensured accuracy across larger datasets. The script now efficiently identifies the minimal column set required for row uniqueness — a solid improvement that pushes the tool closer to full automation.

**Day 5 – Customizing with Dates **
Date: 2025-06-14
Tasks Completed:

Introduced custom validation based on date fields.

Added a date column to both source and destination datasets.

Implemented filtering and validation within a specific date range.

Story:
Today was about tailoring the validation logic to be more flexible and real-world ready. I added a date field to both the source and destination datasets, enabling filtering by a specified range. With this enhancement, the tool can now validate only the rows that fall within a particular date window. This customization makes it highly adaptable for time-bound data checks — a useful step toward making the tool smarter and more context-aware.

Day 6 – Speeding Things Up
Date: 2025-06-15
Tasks Completed:

Implemented multithreading to optimize validation performance.

Measured and logged the time taken for each validation process.

Story:
Performance was the focus today. I integrated multithreading into the validation workflow to handle multiple checks in parallel. This significantly reduced the execution time, especially for larger datasets. To quantify the improvement, I added time tracking for each validation step and logged the duration. Seeing the validation run faster with clean timing logs felt rewarding — the tool is not just functional now, it's efficient.

 Day 7 – Taking It Further with Multiprocessing
Date: 2025-06-16
Tasks Completed:

Switched from multithreading to multiprocessing for heavier validation tasks.

Calculated and compared time taken for validation using multiprocessing.

Story:
After optimizing with multithreading, I explored multiprocessing to push performance even further. Since some validation tasks are CPU-bound, multiprocessing turned out to be a better fit. I refactored the code to run validations in separate processes and tracked the execution time. The difference was noticeable — validations now complete even faster, with better resource utilization. It's satisfying to see the tool evolve from being functional to truly high-performing.


Day 8 – Threads vs. Processes: The Showdown
Date: 2025-06-17
Tasks Completed:

Compared multithreading and multiprocessing performance.

Analyzed execution time and confirmed multiprocessing was faster.

Story:
Today was all about benchmarking. After implementing both multithreading and multiprocessing, I ran them side-by-side to see which one truly performs better for my validation tasks. The results were clear — multiprocessing consistently took less time, especially for CPU-intensive operations. While threads had their use in I/O-bound steps, processes proved more effective for parallel execution of validations. It felt great to validate not just data, but my architectural choices too.

