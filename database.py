# =====================================
# Staff Database
# =====================================

staff = {
    "1001": "Rahamath",
    "1002": "Yashodhare",
    "1003": "Lavanya",
    "1004": "Manik",
    "1005": "Swetha",
    "1006": "Naziya"
}
admins = {
    "9999": "Administrator"
}
# Stores today's attendance
attendance = set()

# Counts visitors
visitor_count = 0


# =====================================
# Staff Attendance
# =====================================

def check_staff(id_number):

    if id_number not in staff:
        return None

    if id_number in attendance:
        return (
            f"Welcome back, {staff[id_number]}!\n\n"
            "Your attendance has already been marked today."
        )

    attendance.add(id_number)

    return (
        f"Welcome, {staff[id_number]}!\n\n"
        "Your attendance has been marked successfully."
    )


# =====================================
# Visitor Counter
# =====================================

def add_visitor():
    global visitor_count

    visitor_count += 1

    return visitor_count


def get_visitor_count():
    return visitor_count


def get_staff_count():
    return len(attendance)
def check_admin(admin_id):
    return admins.get(admin_id)