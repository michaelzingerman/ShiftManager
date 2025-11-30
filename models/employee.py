from config.settings import DAYS, SHIFTS


class Employee:
    def __init__(self, first_name, last_name, role,
                 min_shifts, max_shifts, availability):
        self.first_name = first_name
        self.last_name = last_name
        self.role = role.lower()  # "manager" or "employee"
        self.min_shifts = min_shifts
        self.max_shifts = max_shifts
        self.availability = availability  # dict: {"Mon": ["morning", ...]}
        self.assigned_shifts = []  # list of tuples: (day, shift)

    # ---------------------------------------------------------

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # ---------------------------------------------------------

    def is_available(self, day, shift):
        """Check if worker is available for specific day and shift."""
        if day not in DAYS:
            return False

        available_shifts = self.availability.get(day, [])
        return shift in available_shifts

    # ---------------------------------------------------------

    def shifts_assigned_count(self):
        return len(self.assigned_shifts)

    # ---------------------------------------------------------

    def reached_max_shifts(self):
        return self.shifts_assigned_count() >= self.max_shifts

    # ---------------------------------------------------------

    def will_reach_min_shifts(self):
        return self.shifts_assigned_count() >= self.min_shifts

    # ---------------------------------------------------------

    def has_back_to_back_conflict(self, day, shift):
        """
        If employee worked the previous shift or the shift before that,
        they cannot work this shift.

        Example:
          Sun night → Mon morning is not allowed.
        """
        if not self.assigned_shifts:
            return False

        # Get last assigned shift (day, shift)
        last_day, last_shift = self.assigned_shifts[-1]

        # Find index of current and last day
        try:
            current_day_index = DAYS.index(day)
            last_day_index = DAYS.index(last_day)
        except ValueError:
            return False

        # Case: same day — cannot work consecutive shifts
        if day == last_day:
            return True

        # Case: previous day
        if current_day_index == (last_day_index + 1) % len(DAYS):
            # If last shift ends when new shift starts (no rest)
            if self._shifts_are_consecutive(last_shift, shift):
                return True

        return False

    # ---------------------------------------------------------

    def _shifts_are_consecutive(self, shift1, shift2):
        """
        Helper to check if shift1 → shift2 is consecutive with no rest.
        Example: night → morning
        """
        shifts = list(SHIFTS.keys())
        if shift1 not in shifts or shift2 not in shifts:
            return False

        idx1 = shifts.index(shift1)
        idx2 = shifts.index(shift2)

        # consecutive if shift2 comes right after shift1
        return (idx2 == (idx1 + 1) % len(shifts))

    # ---------------------------------------------------------

    def assign_shift(self, day, shift):
        """Assign a shift to the employee."""
        self.assigned_shifts.append((day, shift))

    # ---------------------------------------------------------

    def __repr__(self):
        return f"Employee({self.full_name()}, {self.role})"
