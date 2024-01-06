import datetime

# Open a file in append mode
with open('/opt/cron_job_test_script_log.txt', 'a') as file:
    # Get the current timestamp
    current_time = datetime.datetime.now()
    # Write the timestamp to the file
    file.write(f"Script executed at: {current_time}\n")
