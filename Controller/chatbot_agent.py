import functools
import json
import time
import traceback
import re
from typing import List
from pydantic import BaseModel, Field

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import create_react_agent

from Controller.main_controller import DM

import os

# Ask for API key interactively if missing (for convenience in local dev)
if not os.getenv("OPENAI_API_KEY"):
    try:
        from getpass import getpass
        key = getpass("Enter your OpenAI API key: ").strip()
        if key:
            os.environ["OPENAI_API_KEY"] = key
            print("[INFO] OpenAI API key set for this session.")
        else:
            print("[WARNING] No API key provided. The chatbot will not function.")
    except Exception:
        print("[ERROR] Could not prompt for API key. Please set OPENAI_API_KEY manually.")


# Tool Argument schemas

class KeyPathArgs(BaseModel):
    key_path: str = Field(
        description="Dot-separated path to the key in the configuration JSON (e.g. faculty[0].name)"
    )
    new_value: str = Field(description="New value (string or JSON).")


class NoArgs(BaseModel):
    pass


class ChatbotAgent:
    def __init__(self, config_path_getter):
        self.get_config_path = config_path_getter

        # Check API key before initializing model
        if not os.getenv("OPENAI_API_KEY"):
            print("[ERROR] OPENAI_API_KEY is not set. The chatbot cannot be initialized.")
            self.model = None
            self.agent_executor = None
            self.disabled = True
            return
        else:
            self.disabled = False

        print("[DEBUG] Initializing ChatbotAgent with OpenAI model...")
        self.model = init_chat_model(
            "gpt-5-mini",
            model_provider="openai",
            temperature=0.2,
            max_tokens=512
        )

        self.tools = self._create_tools()
        print(f"[DEBUG] Registered {len(self.tools)} tools: {[t.name for t in self.tools]}")

        self.agent_executor = create_react_agent(self.model, self.tools)
        print("[DEBUG] ChatbotAgent initialized successfully.\n")

    # Tool Implementations

    def _tool_view_config(self):
        """Return a summarized view of the current configuration (no full details)."""
        print("[DEBUG] Tool called: view_config")
        try:
            if not hasattr(DM, "data") or not DM.data:
                return "No configuration loaded. Please import a config file first."

            config = DM.data.get("config", {})
            summary_lines = []

            # --- Rooms ---
            rooms = config.get("rooms", [])
            summary_lines.append("Rooms:")
            summary_lines += [f"  • {r}" for r in rooms] if rooms else ["  None"]

            # --- Labs ---
            labs = config.get("labs", [])
            summary_lines.append("\nLabs:")
            summary_lines += [f"  • {l}" for l in labs] if labs else ["  None"]

            # --- Courses (only names) ---
            courses = config.get("courses", [])
            summary_lines.append(f"\nCourses ({len(courses)} total):")
            if not courses:
                summary_lines.append("  None found.")
            else:
                seen = set()
                for c in courses:
                    cid = c.get("course_id", "Unknown")
                    if cid not in seen:
                        summary_lines.append(f"  • {cid}")
                        seen.add(cid)

            # Faculty (names only)
            faculty = config.get("faculty", [])
            summary_lines.append(f"\nFaculty ({len(faculty)} total):")
            if not faculty:
                summary_lines.append("  None found.")
            else:
                for f in faculty:
                    if isinstance(f, dict):
                        name = f.get("name") or f.get("faculty_name") or str(f)
                        summary_lines.append(f"  • {name}")
                    else:
                        summary_lines.append(f"  • {str(f)}")

            # Add follow-up question
            summary_lines.append(
                "\nWould you like to see details for any category or specific item?\n"
                "You can ask things like:\n"
                "• 'Show details of all courses'\n"
                "• 'Show details for CMSC 140'\n"
                "• 'Show details for Zoppetti'\n"
            )

            return "\n".join(summary_lines)

        except Exception as e:
            print("[ERROR] view_config summary failed:", e)
            traceback.print_exc()
            return f"Error viewing configuration: {e}"

    def _tool_show_details(self, target: str):
        """Show detailed information for a category or specific entity, with fuzzy and semantic matching."""
        print(f"[DEBUG] Tool called: show_details ({target})")
        try:
            import difflib

            if not hasattr(DM, "data") or not DM.data:
                return "No configuration loaded. Please import a config file first."

            config = DM.data.get("config", {})
            target_clean = target.lower().strip()

            # Clean input and remove filler words
            stopwords = [
                "the", "faculty", "course", "details", "of", "for", "about",
                "show", "me", "all", "information", "info", "available", "list", "view"
            ]
            for w in stopwords:
                target_clean = re.sub(rf"\b{w}\b", "", target_clean)
            target_clean = target_clean.strip()

            result_lines = []

            # Handle all-rooms queries
            if any(x in target.lower() for x in ["all rooms", "rooms", "room list"]):
                rooms = config.get("rooms", [])
                if not rooms:
                    return "No rooms found in the current configuration."
                result_lines.append(f"Showing all {len(rooms)} rooms:\n")
                for r in rooms:
                    result_lines.append(f"• {r}")
                return "\n".join(result_lines)

            # Handle all-labs queries
            if any(x in target.lower() for x in ["all labs", "labs", "lab list"]):
                labs = config.get("labs", [])
                if not labs:
                    return "No labs found in the current configuration."
                result_lines.append(f"Showing all {len(labs)} labs:\n")
                for l in labs:
                    result_lines.append(f"• {l}")
                return "\n".join(result_lines)

            # Handle all-courses queries
            if any(x in target.lower() for x in ["all courses", "courses", "course details"]):
                courses = config.get("courses", [])
                result_lines.append(f"Showing details for all {len(courses)} courses:\n")
                for c in courses:
                    cid = c.get("course_id", "Unknown ID")
                    result_lines.append(
                        f"{cid} ({c.get('credits', '?')} credits)\n"
                        f"Rooms: {', '.join(c.get('room', [])) or 'None'}\n"
                        f"Labs: {', '.join(c.get('lab', [])) or 'None'}\n"
                        f"Faculty: {', '.join(c.get('faculty', [])) or 'None'}\n"
                        f"Conflicts: {', '.join(c.get('conflicts', [])) or 'None'}\n"
                    )
                return "\n".join(result_lines)

            # Handle all-faculty queries
            if any(x in target.lower() for x in ["all faculty", "faculty", "faculty details"]):
                faculty = config.get("faculty", [])
                if not faculty:
                    return "No faculty found in the configuration."
                result_lines.append(f"Showing details for all {len(faculty)} faculty:\n")
                for f in faculty:
                    name = f.get("name") if isinstance(f, dict) else str(f)
                    result_lines.append(f"• {name}")
                return "\n".join(result_lines)

            # Specific course lookup (fuzzy)
            courses = config.get("courses", [])
            course_ids = [c.get("course_id", "").lower() for c in courses]
            close_match = difflib.get_close_matches(target_clean, course_ids, n=1, cutoff=0.6)
            if close_match:
                match = close_match[0]
                for c in courses:
                    if c.get("course_id", "").lower() == match:
                        return (
                            f"{c.get('course_id', 'Unknown ID')} ({c.get('credits', '?')} credits)\n"
                            f"Rooms: {', '.join(c.get('room', [])) or 'None'}\n"
                            f"Labs: {', '.join(c.get('lab', [])) or 'None'}\n"
                            f"Faculty: {', '.join(c.get('faculty', [])) or 'None'}\n"
                            f"Conflicts: {', '.join(c.get('conflicts', [])) or 'None'}"
                        )

            # Specific faculty lookup (fuzzy)
            faculty = config.get("faculty", [])
            faculty_names = [
                (f.get("name") if isinstance(f, dict) else str(f)) for f in faculty
            ]
            faculty_lower = [name.lower() for name in faculty_names]
            close_match = difflib.get_close_matches(target_clean, faculty_lower, n=1, cutoff=0.6)
            if close_match:
                match_index = faculty_lower.index(close_match[0])
                return f"Faculty: {faculty_names[match_index]}"

            # Room or lab single-item fuzzy lookup
            all_rooms = [r.lower() for r in config.get("rooms", [])]
            all_labs = [l.lower() for l in config.get("labs", [])]

            match_room = difflib.get_close_matches(target_clean, all_rooms, n=1, cutoff=0.7)
            if match_room:
                return f"Room: {match_room[0].title()}"

            match_lab = difflib.get_close_matches(target_clean, all_labs, n=1, cutoff=0.7)
            if match_lab:
                return f"Lab: {match_lab[0].title()}"

            # Default fallback
            return f"No matching item found for '{target}'. Try 'all rooms', 'all labs', 'all courses', or a name."

        except Exception as e:
            print("[ERROR] show_details failed:", e)
            traceback.print_exc()
            return f"Error showing details: {e}"

    def _tool_update_config_value(self, key_path: str, new_value: str):
        """Modify the configuration in DM.data and save."""
        print(f"[DEBUG] Tool called: update_config_value ({key_path} = {new_value})")
        try:
            if not hasattr(DM, "data") or not DM.data:
                return "No configuration loaded. Please import a config file first."

            # Navigate into DM.data using dot/bracket notation
            keys = key_path.split(".")
            ref = DM.data
            for k in keys[:-1]:
                if "[" in k and "]" in k:
                    name, idx = k[:-1].split("[")
                    ref = ref[name][int(idx)]
                else:
                    ref = ref[k]

            final_key = keys[-1]
            parsed_value = json.loads(new_value) if new_value.strip().startswith(("{", "[", '"')) else new_value
            if "[" in final_key and "]" in final_key:
                name, idx = final_key[:-1].split("[")
                ref[name][int(idx)] = parsed_value
            else:
                ref[final_key] = parsed_value

            # Persist changes using DataManager
            DM.saveData(self.get_config_path())
            return f"Updated {key_path} successfully."
        except Exception as e:
            print("[ERROR] update_config_value failed:", e)
            traceback.print_exc()
            return f"Error updating config: {e}"

    # Tool registration

    def _create_tools(self) -> List[StructuredTool]:
        return [
            StructuredTool.from_function(
                name="view_config",
                func=self._tool_view_config,
                description="Display the current scheduler configuration summary.",
                args_schema=NoArgs,
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="update_config_value",
                func=self._tool_update_config_value,
                description="Update a field in the configuration using dot notation.",
                args_schema=KeyPathArgs,
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="show_details",
                func=self._tool_show_details,
                description="Show detailed information for a specific item or category (e.g., all courses, Zoppetti, CMSC 140).",
                return_direct=True,
            ),
        ]

    # Query endpoint

    def query(self, user_input: str) -> str:
        if getattr(self, "disabled", False):
            return "The AI Chatbot is disabled because no OpenAI API key was set."

        try:
            text = (user_input or "").strip()

            # Direct detail commands
            if text.lower().startswith("show details"):
                target = re.sub(r"show details( of| for)?", "", text, flags=re.I).strip() or "all courses"
                return self._tool_show_details(target)

            # Greetings / small talk
            if re.fullmatch(r"(hi|hello|hey|howdy|yo|sup)\W*", text.lower()):
                return (
                    "Hi! I can help with the scheduler configuration.\n"
                    "• View the current config (rooms, labs, courses, faculty)\n"
                    "• Make a change (e.g., “remove Mac lab from CMSC 330”)\n"
                    "• Explain what a field does\n\n"
                    "What would you like to do?"
                )

            print(f"\n[DEBUG] Query started: {user_input}")

            system_message = SystemMessage(
                content=(
                    "You are the academic scheduling assistant.\n"
                    "Only use tools when explicitly requested by the user (view/change/show details).\n"
                    "Use 'view_config' to summarize the configuration in plain text (not JSON)."
                )
            )

            start = time.time()
            result = self.agent_executor.invoke({"messages": [system_message, HumanMessage(content=user_input)]})
            elapsed = time.time() - start
            print(f"[DEBUG] Agent call completed in {elapsed:.2f}s")

            # Universal Extractor
            response = None

            if isinstance(result, dict):
                # Direct top-level fields
                for key in ["output", "return_values", "final_output"]:
                    if key in result and result[key]:
                        response = str(result[key])
                        print(f"[DEBUG] Found response in result['{key}']")
                        break

                # Search inside messages (covers ToolMessage & AIMessage)
                if not response and "messages" in result:
                    for m in result["messages"]:
                        msg_dict = (
                            m.__dict__
                            if hasattr(m, "__dict__")
                            else m
                            if isinstance(m, dict)
                            else {}
                        )

                        # a) ToolMessage case (the most common for tool output)
                        if getattr(m, "__class__", type(m)).__name__ == "ToolMessage" or msg_dict.get("name"):
                            if "content" in msg_dict and msg_dict["content"]:
                                response = msg_dict["content"]
                                print("[DEBUG] Found response in ToolMessage.content")
                                break

                        # b) Direct content with summary keywords
                        if "content" in msg_dict and msg_dict["content"]:
                            content = msg_dict["content"]
                            if isinstance(content, str) and any(
                                    k in content for k in ["Rooms:", "Labs:", "Courses", "Faculty", "Showing details"]
                            ):
                                response = content
                                print("[DEBUG] Found response in message.content (tool text)")
                                break

                        # c) Embedded outputs in additional_kwargs
                        extras = msg_dict.get("additional_kwargs", {})
                        if extras:
                            for k, v in extras.items():
                                if isinstance(v, str) and any(
                                        kw in v for kw in ["Rooms:", "Labs:", "Courses", "Faculty", "Showing details"]
                                ):
                                    response = v
                                    print(f"[DEBUG] Found response in message.additional_kwargs['{k}']")
                                    break
                            if response:
                                break

                # LangGraph “tool_calls” fallback
                if not response and "tool_calls" in result:
                    response = str(result["tool_calls"])
                    print("[DEBUG] Found response in result['tool_calls']")

            # Default fallback
            if not response or not str(response).strip():
                print("[DEBUG] Could not extract tool output; dumping message structure:")
                from pprint import pprint
                pprint(result.get("messages", []))
                response = "(No response received.)"

            print(f"[DEBUG] Final resolved response:\n{response[:500]}...")
            return response

        except Exception as e:
            print("[ERROR] query() exception:", e)
            traceback.print_exc()
            return f"Error: {e}"