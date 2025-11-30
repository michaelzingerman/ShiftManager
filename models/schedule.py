import pandas as pd
from config.settings import (
    DAYS, SHIFTS,
    MANAGERS_PER_SHIFT,
    EMPLOYEES_PER_SHIFT
)


class Schedule:
    def __init__(self):
        """
        Creates a structure:
        schedule[day][shift] = {
            "managers": [Employee1, ...],
            "employees": [Employee2, ...]
        }
        """
        self.schedule = {
            day: {
                shift: {
                    "managers": [],
                    "employees": []
                }
                for shift in SHIFTS.keys()
            }
            for day in DAYS
        }

    # -----------------------------------------------------

    def shift_is_full(self, day, shift, role):
        """
        Check if the shift already has the required number of workers.
        """
        slot = self.schedule[day][shift]

        if role == "manager":
            return len(slot["managers"]) >= MANAGERS_PER_SHIFT

        elif role == "employee":
            return len(slot["employees"]) >= EMPLOYEES_PER_SHIFT

        return True  # unknown role → treat as full

    # -----------------------------------------------------

    def add_worker(self, employee, day, shift):
        """
        Add worker to the schedule, based on role.
        """
        role = employee.role

        if role == "manager":
            self.schedule[day][shift]["managers"].append(employee)
        else:
            self.schedule[day][shift]["employees"].append(employee)

    # -----------------------------------------------------

    def to_dataframe(self):
        """
        Convert schedule into a DataFrame readable by humans.

        Example output:
                    morning               evening                   night
        Mon   Manager: John     Manager: Dana        Manager: Sarah
              Emp: Adam,Lior   Emp: Guy,Maya,...    Emp: ...
        """
        data = {shift: [] for shift in SHIFTS.keys()}

        for day in DAYS:
            for shift in SHIFTS.keys():
                slot = self.schedule[day][shift]

                managers = ", ".join([m.full_name() for m in slot["managers"]])
                employees = ", ".join([e.full_name() for e in slot["employees"]])

                cell_text = f"Mgr: {managers}\nEmp: {employees}"
                data[shift].append(cell_text)

        df = pd.DataFrame(data, index=DAYS)
        return df

    # -----------------------------------------------------

    def __repr__(self):
        return str(self.to_dataframe())
