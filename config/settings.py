# config/settings.py

# Days of the week (customizable)
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Default shifts (customizable)
SHIFTS = {
    "morning": ("07:00", "15:00"),
    "evening": ("15:00", "23:00"),
    "night": ("23:00", "07:00")
}

# Minimum number of shifts each employee must work per week
MIN_GLOBAL_SHIFTS = 3

# Maximum shifts per worker per week (default)
DEFAULT_MAX_SHIFTS = 7

# Staffing requirements per shift
MANAGERS_PER_SHIFT = 1
EMPLOYEES_PER_SHIFT = 4   # can change any time

# Formatting / parsing settings
AVAILABILITY_SEPARATOR_DAYS = ";"
AVAILABILITY_SEPARATOR_SHIFTS = ","
