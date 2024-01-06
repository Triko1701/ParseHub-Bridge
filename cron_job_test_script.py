from utils.time import get_time

# Open a file in append mode
with open('/opt/cron_job_test_file.txt', 'a') as file:
    # Get the current timestamp
    current_time = get_time()
    # Write the timestamp to the file
    file.write(f"Script executed at: {current_time}\n")
