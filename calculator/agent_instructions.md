# Durable Project Knowledge Instruction File

## Purpose
This file serves as a reference for the AI coding agent to maintain consistent behavior across sessions, handle user requests efficiently, and ensure reliable use of the available tools.

## 1. Agent Overview
- **Role**: Assist users with coding tasks, file manipulation, and Python execution.
- **Scope**: Operates within the provided working directory and uses the defined toolset.
- **Durability**: All instructions are stored in this file to persist across restarts.

## 2. Tool Usage
| Tool | Purpose | Typical Use Cases |
|------|---------|-------------------|
| `get_files_info` | List files/directories with size and type | Inspect project structure |
| `get_file_content` | Read file contents | Review code, documentation |
| `run_python_file` | Execute a Python script | Run tests, generate outputs |
| `write_file` | Create or overwrite a file | Add new modules, update docs |

### 2.1. Calling Tools
- Always provide the required arguments.
- Use relative paths; the working directory is implicit.
- Validate responses before proceeding.

## 3. Task Planning
1. **Parse the request** – Identify the goal, required files, and actions.
2. **Check prerequisites** – Verify that necessary files exist or create them.
3. **Plan steps** – Break the task into atomic operations.
4. **Execute sequentially** – Call tools in order, handling errors.
5. **Confirm success** – Verify output or file changes.
6. **Return a concise summary** – Provide the user with results or next steps.

## 4. Error Handling
- If a tool returns an error, log the message and attempt a retry if appropriate.
- For non-recoverable errors, explain the issue to the user and suggest manual intervention.
- Avoid infinite loops; limit retries to 3 attempts.

## 5. State Management
- Do not rely on external state; always read from the filesystem.
- Use temporary files only when necessary and clean them up after use.
- Keep a `log.txt` file for debugging if needed.

## 6. Security & Safety
- Do not execute arbitrary code unless explicitly requested.
- Validate file paths to prevent directory traversal.
- Do not write or execute files outside the working directory.

## 7. Documentation & Logging
- After creating or modifying a file, add a comment header with the date and purpose.
- Maintain a `CHANGELOG.md` for major changes.
- Use `write_file` to append logs to `log.txt`.

## 8. Future Prompt Handling
- Store frequently used patterns in this file for quick reference.
- When encountering ambiguous requests, ask clarifying questions before proceeding.
- Keep the instruction set up-to-date with new tools or workflow changes.

## 9. Versioning
- **Version**: 1.0.0
- **Last Updated**: 2026-10-20

---

Feel free to reference this file whenever you need guidance on how to proceed with a task.
