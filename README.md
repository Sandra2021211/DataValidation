**Day 1** – Column Mapping

Date: 2025-06-10

Highlights: 1. Validated column mappings between source and destination files using mapping.json.

            2. Detected unmapped columns through set operations and logged discrepancies.
            
Summary: Started building the data validation tool by aligning column names between source and destination files. Extracted column names, compared them, and logged unmapped ones if any. This foundational task set the stage for accurate data validation.

**Day 2** – Data Integrity Checks

Date: 2025-06-11

Highlights: 1. Checked for empty rows and duplicate entries.

            2. Validated data types for mapped columns.
            
            3. Compared row and column counts using df.shape().
            
Summary: Enhanced data integrity by removing empty rows, identifying duplicates, and validating data types between source and destination. Structural discrepancies were caught early, ensuring clean data for further validation steps.

**Day 3** – Unique Key Identification

Date: 2025-06-12

Highlights: 1. Found a unique key by combining columns iteratively.

            2. Ensured row-level uniqueness for future validations.
            
Summary: Determined a unique identifier for each row by testing single and multi-column combinations. This hands-on process deepened my understanding of the dataset’s structure and prepared it for precise row-level validation.
