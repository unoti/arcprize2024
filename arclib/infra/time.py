from datetime import datetime
from typing import Optional


def timestamp_string(dt: Optional[datetime] = None):
    """Create a timestamp as a string suitable for using in time-based filenames in YYYYMMDD-hhmm format.
    """
    if not dt:
        dt = datetime.now()
    return dt.strftime('%Y%m%d-%H%M')