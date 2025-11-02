# chatbot_cli.py
from Controller.main_controller import RoomsController, LabsController, CourseController, FacultyController
from Models.Data_manager import DataManager

def main():
    print("Chatbot CLI for Schedule Manager")
    print("Type 'exit' to quit.\n")

    DM = DataManager()
    labs_ctrl = LabsController()
    rooms_ctrl = RoomsController()
    courses_ctrl = CourseController()
    faculty_ctrl = FacultyController()

    while True:
        user_input = input("Enter a query: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = handle_query(user_input, labs_ctrl, rooms_ctrl, courses_ctrl, faculty_ctrl)
        print(response)

def handle_query(query, labs_ctrl, rooms_ctrl, courses_ctrl, faculty_ctrl):
    query_lower = query.lower()

    # --- Add labs ---
    if query_lower.startswith("add the following labs"):
        names = [n.strip() for n in query.split(":")[1].split(",")]
        responses = []
        for lab in names:
            labs_ctrl.addLab(lab, lambda _: None)
            responses.append(f"Lab {lab} added successfully")
        return "\n".join(responses)

    # --- Rename lab ---
    if "rename" in query_lower and "lab" in query_lower:
        try:
            parts = query.split('"')
            old, new = parts[1], parts[3]
            if new in labs_ctrl.listLabs():
                return f"Lab {new} already exists so it cannot be renamed from {old}"
            labs_ctrl.editLab(old, new, lambda **_: None)
            return f"Lab {old} renamed to {new} successfully"
        except Exception:
            return "Invalid rename command format."

    # --- Add courses ---
    if query_lower.startswith("add the following courses"):
        prefix = "CMSC"
        names = [n.strip() for n in query.split(":")[1].split(",")]
        responses = []
        for course in names:
            full_name = f"{prefix} {course}"
            courses_ctrl.addCourse({"name": full_name}, lambda _: None)
            responses.append(f"Course {full_name} added successfully")
        return "\n".join(responses)

    # --- Add rooms ---
    if query_lower.startswith("add the following rooms"):
        names = [n.strip() for n in query.split(":")[1].split(",")]
        responses = []
        for room in names:
            rooms_ctrl.addRoom(room, lambda _: None)
            responses.append(f"Room {room} added successfully")
        return "\n".join(responses)

    # --- Fallback ---
    return "Sorry, I didn't understand that command."

if __name__ == "__main__":
    main()
