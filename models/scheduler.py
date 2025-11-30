
from config.settings import DAYS, SHIFTS, MIN_GLOBAL_SHIFTS
from models.schedule import Schedule


class Scheduler:
    def __init__(self, employees):
        """
        employees = list of Employee objects
        """
        self.employees = employees
        self.schedule = Schedule()

        self.managers = [e for e in employees if e.role == "manager"]
        self.workers = [e for e in employees if e.role == "employee"]

    # --------------------------------------------------------------

    def run(self):
        """
        Main scheduling loop.
        Assign managers first, then regular employees.
        """
        for day in DAYS:
            for shift in SHIFTS.keys():
                self.assign_managers(day, shift)
                self.assign_workers(day, shift)

        return self.schedule

    # --------------------------------------------------------------

    def assign_managers(self, day, shift):
        """
        Assign managers to the shift.
        """
        for manager in self.managers:

            if self.schedule.shift_is_full(day, shift, role="manager"):
                return  # already filled

            if not manager.is_available(day, shift):
                continue

            if manager.reached_max_shifts():
                continue

            if manager.has_back_to_back_conflict(day, shift):
                continue

            # Assign manager
            manager.assign_shift(day, shift)
            self.schedule.add_worker(manager, day, shift)

    # --------------------------------------------------------------

    def assign_workers(self, day, shift):
        """
        Assign regular employees to the shift.
        """
        for worker in self.workers:

            if self.schedule.shift_is_full(day, shift, role="employee"):
                return  # already filled all employee slots

            if not worker.is_available(day, shift):
                continue

            if worker.reached_max_shifts():
                continue

            if worker.has_back_to_back_conflict(day, shift):
                continue

            # Assign employee
            worker.assign_shift(day, shift)
            self.schedule.add_worker(worker, day, shift)

    # --------------------------------------------------------------

    def validate_min_shifts(self):
        """
        Check if all workers reached the global minimum number of shifts.
        Return list of workers who did NOT meet the requirement.
        """
        underworked = []
        for e in self.employees:
            if e.shifts_assigned_count() < MIN_GLOBAL_SHIFTS:
                underworked.append(e)
        return underworked

    # --------------------------------------------------------------

    def print_summary(self):
        """
        Print summary of shifts assigned to each worker.
        """
        for e in self.employees:
            print(f"{e.full_name()}: {e.shifts_assigned_count()} shifts")
