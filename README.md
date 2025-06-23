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