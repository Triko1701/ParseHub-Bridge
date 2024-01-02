from datetime import datetime
import pytz

def get_time():
    # Sydney Timezone
    sydney_tz = pytz.timezone('Australia/Sydney')
    # Sydney Time
    time_sydney = datetime.now(sydney_tz)
    return time_sydney