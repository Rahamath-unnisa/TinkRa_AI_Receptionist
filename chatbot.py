from knowledge import knowledge
from database import (
    check_staff,
    add_visitor,
    check_admin,
    get_visitor_count,
    get_staff_count
)

admin_mode = False
def get_response(user_input):
    global admin_mode
    text = user_input.lower().strip()

    # ===========================
    # Staff ID
    # ===========================
    if text == "admin":

        admin_mode = True

        return "Please enter the Admin ID."
    if admin_mode and text.isdigit():

        admin = check_admin(text)

        admin_mode = False

        if admin:

            return (
                f"Welcome {admin}.\n\n"
                f"Today's Dashboard\n\n"
                f"👥 Visitors : {get_visitor_count()}\n"
                f"👨‍💼 Staff : {get_staff_count()}"
            )

        return "Invalid Admin ID."
    if text.isdigit():

        response = check_staff(text)

        if response:
            return response

        return "Invalid Staff ID.\n\nPlease try again."

    # ===========================
    # Visitor
    # ===========================
    if "visitor" in text:

        count = add_visitor()

        return (
            f"Welcome to TinkEdge Robotics Lab!\n\n"
            "How may I help you today?"
        )

    # ===========================
    # Knowledge Base
    # ===========================
    for keywords, response in knowledge.items():

        for word in keywords:

            if word in text:
                return response

    # ===========================
    # Default
    # ===========================
    return (
        "I'm sorry.\n\n"
        "I couldn't understand that.\n"
        "Could you please ask in another way?"
    )