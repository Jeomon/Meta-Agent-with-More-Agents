**Package Installer**

Analyze the user's query to determine the appropriate Python library. Generate the corresponding bash command using `pip` to install the library, and return the response in JSON format.

**Query:** {query}

Respond in the following JSON format:
```json
{{
      "command": "pip install <python_library_name>"
}}
```