# chatbot_cli.py

import json
import os
from Controller.chatbot_agent import ChatbotAgent
from Models.Data_manager import DataManager


def save_config(DM, path):
    """Save the current DM.data structure back to disk."""
    try:
        with open(path, "w") as f:
            json.dump(DM.data, f, indent=4)
        print(f"Configuration saved to {path}")
    except Exception as e:
        print(f"Failed to save config: {e}")


def main(cfg_path=None):
    print("=" * 60)
    print("Welcome to the Chatbot CLI for Schedule Manager")
    print("=" * 60)
    print("Type your commands in plain English!")
    print("Examples:")
    print("  • add a room called Roddy 1")
    print("  • add a lab called Mac")
    print("  • add a faculty named Hobbs with 4 min credits and 8 max credits")
    print("  • add a course named CMSC 123 that's 5 credits.")
    print("  • delete course CMSC 123")
    print("\nType 'exit' or 'quit' to leave.\n")

    # --- Use provided path or fallback ---
    if not cfg_path:
        cfg_path = "output/mainConfig.json"

    # --- Load DataManager Config ---
    from Controller.main_controller import DM

    if os.path.exists(cfg_path):
        with open(cfg_path, "r") as f:
            DM.data = json.load(f)
            print(f"Config loaded from {cfg_path}")
    else:
        DM.data = {"config": {"rooms": [], "labs": [], "courses": [], "faculty": []}}
        print("No config file found. Starting with an empty config.")

    # 🔧 Ensure ChatbotAgent uses this same populated DataManager
    import Controller.main_controller as ctrl
    ctrl.DM = DM

    # --- Initialize chatbot agent ---
    agent = ChatbotAgent(lambda: cfg_path)
    agent.disabled = False

    # --- CLI main loop ---
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            if not user_input:
                continue

            result = agent.query(user_input)

            # --- Pretty-print response ---
            if isinstance(result, dict):
                print(f"\nChatbot: {result.get('response', 'No response.')}")
                if result.get("payload"):
                    print(json.dumps(result["payload"], indent=2))

                # --- Auto-save after successful modify ---
                if not result.get("error") and result.get("action") in (
                    "add",
                    "edit",
                    "delete",
                ):
                    save_config(DM, cfg_path)

            else:
                print(f"\nChatbot: {result}")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
