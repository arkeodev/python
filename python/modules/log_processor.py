# Imports
from datetime import datetime
from multiprocessing import Pool

# Step 1: Reading the Large Log File
def read_large_file(file_path):
    '''
    Reads the file line by line, yielding each line. This is memory 
    efficient as it doesn't load the entire file into memory.
    '''
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

# Step 2: Filtering Error Entries
def filter_errors(log_lines):
    '''
    Filters out log lines that do not contain the keyword "ERROR".
    '''
    for line in log_lines:
        if "ERROR" in line:
            yield line

# Step 3: Extracting Relevant Information
def extract_info(error_lines):
    '''
    Splits each log line into its components and yields the timestamp 
    and error message.
    '''
    for line in error_lines:
        parts = line.split(' - ')
        if len(parts) >= 3:
            timestamp, log_level, message = parts[0], parts[1], parts[2]
            yield timestamp, message

# Step 4: Transforming Data in Parallel
def transform_entry(entry):
    '''
    Performs the transformation for a single log entry.
    '''
    timestamp, message = entry
    new_timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')
    return new_timestamp, message

def transform_data_parallel(log_entries, pool_size=4):
    '''
    Uses the `Pool` class from the `multiprocessing` module to parallelize 
    the transformation step. The `imap` method allows for lazy iteration 
    over the results as they are computed, maintaining the benefits of 
    generator-based processing.
    '''
    with Pool(pool_size) as pool:
        for result in pool.imap(transform_entry, log_entries, chunksize=100):
            yield result

# Step 5: Writing to a New File
def write_processed_data(processed_data, output_file_path):
    '''
    Writes the processed data to a new file, line by line.
    '''
    with open(output_file_path, 'w') as file:
        for timestamp, message in processed_data:
            file.write(f"{timestamp} - ERROR - {message}\n")

# Step 6: Combining Everything into a Pipeline
def process_log_file(input_file_path, output_file_path):
    '''
    Ties all the steps together, creating a parallelized data processing pipeline.
    '''
    log_lines = read_large_file(input_file_path)
    error_lines = filter_errors(log_lines)
    log_entries = extract_info(error_lines)
    transformed_entries = transform_data_parallel(log_entries)
    write_processed_data(transformed_entries, output_file_path)

if __name__ == '__main__':
    # Usage example
    input_file_path = './data/large_log_file.txt'
    output_file_path = './data/processed_errors.txt'
    process_log_file(input_file_path, output_file_path)

    # Verify the output
    with open(output_file_path, 'r') as file:
        print(file.read())