from datetime import datetime
import pytz

def get_time(tz: str='Australia/Sydney'):
    # Sydney Timezone
    tz = pytz.timezone(tz)
    # Sydney Time
    time = datetime.now(tz)
    return time