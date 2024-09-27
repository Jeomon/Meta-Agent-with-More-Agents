# Meta Agent with More Agents: AI Task Delegation Workflow

## Description

**Meta Agent with More Agents** is a project designed to dynamically delegate complex queries to specialized AI agents. At the core of the system is the **Meta Agent**, which orchestrates the problem-solving process by breaking down queries into sub-tasks and assigning each to the most suitable agent. These agents either solve sub-tasks using tools (via the **ReAct Agent**) or by reasoning step-by-step (via the **Chain of Thought Agent**). The Meta Agent continues this iterative process until the entire task is solved, providing the final answer to the user.

## Architecture Overview

![Image of the Workflow](diagram.svg)

The project employs a hierarchical and flexible design:

- **Meta Agent:** Manages the overall query-solving process by determining how to break down tasks and assigning them to appropriate agents based on the task's requirements.
- **ReAct Agent:** Handles tasks that require external tools. It either executes the query with existing tools or, when needed, requests tool creation, updates, or deletions via the **Tool Agent**.
- **Tool Agent:** Dynamically creates, updates, or deletes tools required by the ReAct Agent to handle specific tasks. It can remove a tool if it fails to work correctly, doesn't produce the intended output even after debugging, or if the user requests its removal.
- **Chain of Thought (CoT) Agent:** Processes tasks that do not require external tools, solving them through an iterative reasoning approach.

This architecture ensures smooth communication between agents and enables dynamic tool creation, updating, or deletion to expand the problem-solving capabilities.

### Workflow

1. The **Meta Agent** receives a query.
2. It analyzes the task and determines whether it requires tools or iterative reasoning:
   - If tools are needed, the **ReAct Agent** is invoked.
   - If no tools are required, the **CoT Agent** is engaged.
3. If the **ReAct Agent** determines that a required tool is missing or not functioning, it invokes the **Tool Agent** to create, update, or delete the tool.
4. Sub-tasks are solved incrementally, with results passed back to the **Meta Agent**.
5. The process continues until the entire query is resolved.

## Key Features

- **Dynamic Task Delegation:** Automatically assigns sub-tasks to specialized agents based on task type and complexity.
- **Tool Creation, Updates, & Deletion:** The **Tool Agent** can dynamically generate, update, or delete tools at runtime based on task requirements or failures.
- **Iterative Reasoning (Chain of Thought):** Solves tasks without tools by breaking them down into smaller reasoning steps.
- **Hierarchical Problem Solving:** Complex queries are divided into smaller, manageable sub-tasks that are solved iteratively.
- **Modular Design:** Agents can be easily expanded or replaced, allowing for flexibility and scalability.

## Tool Deletion Feature

In addition to creating and updating tools, the **Tool Agent** has the ability to delete tools when necessary. The **ReAct Agent** can request the **Tool Agent** to remove a tool under the following circumstances:
- The tool is failing or not producing the desired output.
- Debugging efforts are unsuccessful.
- The user requests to remove the tool.

This ensures that non-functional tools do not hinder the system's performance, and the workflow remains efficient.

## Installation

To set up the project, ensure you have Python 3.x installed, then run the following command to install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

To run the ReAct Agent with Tool Agent, execute the following command:

```bash
python app.py
```

## Usage

To start using **Meta Agent with More Agents**, follow these steps:

1. Provide a query to the **Meta Agent**.
2. The **Meta Agent** will create a system prompt and assign the task to either the **ReAct Agent** (if tools are required) or the **CoT Agent** (if the task relies on reasoning).
3. If tools are missing, outdated, or non-functional, the **Tool Agent** will dynamically create, update, or remove them.
4. Sub-tasks are solved iteratively, with results compiled and provided as a final answer to the user.

### Example Queries

#### Example 1: Search the web and save it to a file.

```plaintext
Enter a query: Can you searach the web and structure the information for health is wealth and save it to health.txt in current working directory.
Entering Meta Agent
Agent Name: Web Search Agent
Description: This agent will search the web for information related to "health is wealth" and structure the information.
Tasks: ['Search the web for relevant information related to "health is wealth".', 'Structure the information in a clear and readable format.', 'Save the structured information to a text file named "health.txt" in the current working directory.']
Tool: {'Tool Name': 'Web Search Tool', 'Tool Description': 'A tool that allows the agent to search the web for information.'}
Entering Web Search Agent
Thought: Since the task requires searching the web for information related to "health is wealth" and structuring the information, I need a tool that can perform web searches and structure the results. However, the available tools in the tool box do not include a web search tool. Therefore, I will request the creation of a new tool that can perform this task.
Entering Tool Agent
Query: Create a new tool called "Web Search Tool" that can search the web for information related to a given topic and structure the results in a clear and readable format. This tool should be able to handle topics like "health is wealth" and provide structured information.
Web Search Tool has been saved to experimental.py successfully.
Tool Name: Web Search Tool
Tool Input: {'properties': {'query': {'description': 'The topic to be searched.', 'example': ['health is wealth'], 'title': 'Query', 'type': 'string'}}, 'required': ['query'], 'type': 'object'}
 Tool has been generated successfully. Now the tool is available in the tool box and ready for use.
Thought: Now that the Web Search Tool is available in the tool box, I can use it to search the web for information related to "health is wealth" and structure the results. I will provide the query as input to the tool and retrieve the structured information.
Action Name: Web Search Tool
Action Input: {
  "query": "health is wealth"
}
Observation: No module named 'duckduckgo_search'
Thought: The Web Search Tool is encountering an error due to a missing module named 'duckduckgo_search'. This module is likely required for the tool to function properly. To resolve this issue, I will request the installation of the missing Python package.
Entering Tool Agent
Query: Install the missing Python package 'duckduckgo_search' required for the Web Search Tool to function properly.     
Collecting duckduckgo_search
  Downloading duckduckgo_search-6.2.13-py3-none-any.whl.metadata (25 kB)
Requirement already satisfied: click>=8.1.7 in d:\personal projects\meta-agent-with-more-agents\.venv\lib\site-packages (from duckduckgo_search) (8.1.7)
Collecting primp>=0.6.3 (from duckduckgo_search)
  Downloading primp-0.6.3-cp38-abi3-win_amd64.whl.metadata (10 kB)
Requirement already satisfied: colorama in d:\personal projects\meta-agent-with-more-agents\.venv\lib\site-packages (from click>=8.1.7->duckduckgo_search) (0.4.6)
Downloading duckduckgo_search-6.2.13-py3-none-any.whl (27 kB)
Downloading primp-0.6.3-cp38-abi3-win_amd64.whl (2.8 MB)
   ---------------------------------------- 2.8/2.8 MB 2.9 MB/s eta 0:00:00
Installing collected packages: primp, duckduckgo_search
Successfully installed duckduckgo_search-6.2.13 primp-0.6.3
attribute name must be string, not 'NoneType'
Package installed successfully. Now the tool is available in the tool box and ready for use.
Thought: Now that the missing package has been installed, I can retry using the Web Search Tool to search the web for information related to "health is wealth" and structure the results. I will provide the query as input to the tool and retrieve the structured information.
Action Name: Web Search Tool
Action Input: {
  "query": "health is wealth"
}
Observation: Health Is Wealth: What It Means and Why It's True
Learn how your physical and mental well-being is more important than wealth for life satisfaction and financial success. Find out how being healthy can save you money, boost your income, and prevent debt.
7 Reasons Why Health Is Wealth - The STRIVE
Learn the meaning and benefits of health is wealth, a proverb that emphasizes the importance of optimal wellbeing over money. Discover seven reasons why health is wealth and how to achieve it with fitness, lifestyle, and happiness.
The Deep Connection Between Your Health And Wealth - Forbes
Learn how health and wealth are interrelated and how to assess, improve and safeguard both. Find out the benefits of regular checks, expert advice and action plans for your financial and physical well-being.
Why 'Health is Wealth' is More Than Just a Saying
In conclusion, "Health is Wealth" is more than just a saying. Good health is the foundation of a prosperous and fulfilling life. By prioritizing health, you can achieve financial stability ...
Health is Wealth: Proverb Meaning and Expansion of idea
Learn the meaning, origin, and importance of the proverb "health is wealth" with examples and stories. Find out how health gives you the strength and opportunity to achieve your goals and dreams.
Thought: Now that I have the structured information from the Web Search Tool, I can provide the final answer to the user. The information retrieved highlights the importance of health over wealth, emphasizing how physical and mental well-being can lead to life satisfaction, financial success, and overall prosperity.
Answer: # Health is Wealth: Understanding the Importance of Physical and Mental Well-being

The phrase "health is wealth" is more than just a saying; it's a way of life. Prioritizing health can lead to financial stability, life satisfaction, and overall prosperity. Here are some key points to consider:

* **Physical and mental well-being are crucial for life satisfaction**: Good health gives you the strength and opportunity to achieve your goals and dreams.
* **Health can save you money, boost your income, and prevent debt**: By being healthy, you can avoid medical expenses, increase your earning potential, and make better financial decisions.
* **There's a deep connection between health and wealth**: Regular health checks, expert advice, and action plans can help you assess, improve, and safeguard both your physical and financial well-being.
* **Prioritizing health can lead to financial stability**: By focusing on your health, you can achieve financial stability and prosperity.

In conclusion, "health is wealth" is a proverb that emphasizes the importance of optimal well-being over money. By prioritizing health, you can achieve financial stability, life satisfaction, and overall prosperity.
Agent Name: File Writer Agent
Description: This agent will save the structured information to a text file named "health.txt" in the current working directory.
Tasks: ['Open a new file named "health.txt" in the current working directory.', 'Write the provided text to the file.', 'Close the file to ensure the data is saved.']
Tool: {'Tool Name': 'File Writer Tool', 'Tool Description': 'A tool that allows the agent to write text to a file.'}     
Entering File Writer Agent
Thought: Since the task is to save the provided text to a file named "health.txt" in the current working directory, I need a tool that can write to a file. However, the available tool in the tool box is the "User Interaction Tool" which is not suitable for this task. Therefore, I will request a new tool that can write to a file.
Entering Tool Agent
Query: Please create a new tool called "File Writer Tool" that can write the provided text to a file named "health.txt" in the current working directory. The tool should take the file name and the text to be written as input.
File Writer Tool has been saved to experimental.py successfully.
Tool Name: File Writer Tool
Tool Input: {'properties': {'file_name': {'description': 'The name of the file to be written.', 'example': ['health.txt'], 'title': 'File Name', 'type': 'string'}, 'text': {'description': 'The text to be written to the file.', 'example': ['Hello, World!'], 'title': 'Text', 'type': 'string'}}, 'required': ['file_name', 'text'], 'type': 'object'}
 Tool has been generated successfully. Now the tool is available in the tool box and ready for use.
Thought: Now that the "File Writer Tool" is available in the tool box, I can use it to write the provided text to a file named "health.txt" in the current working directory.
Action Name: File Writer Tool
Action Input: {
  "file_name": "health.txt",
  "text": "# Health is Wealth: Understanding the Importance of Physical and Mental Well-being\n\nThe phrase \"health is wealth\" is more than just a saying; it's a way of life. Prioritizing health can lead to financial stability, life satisfaction, and overall prosperity. Here are some key points to consider:\n\n* **Physical and mental well-being are crucial for life satisfaction**: Good health gives you the strength and opportunity to achieve your goals and dreams.\n* **Health can save you money, boost your income, and prevent debt**: By being healthy, you can avoid medical expenses, increase your earning potential, and make better financial decisions.\n* **There's a deep connection between health and wealth**: Regular health checks, expert advice, and action plans can help you assess, improve, and safeguard both your physical and financial well-being.\n* **Prioritizing health can lead to financial stability**: By focusing on your health, you can achieve financial stability and prosperity.\n\nIn conclusion, \"health is wealth\" is a proverb that emphasizes the importance of optimal well-being over money. By prioritizing health, you can achieve financial stability, life satisfaction, and overall prosperity."
}
Observation: Text successfully written to health.txt.
Thought: Now that the text has been successfully written to the file "health.txt", I can provide the final answer to the user.
Answer: The provided text has been successfully saved to a file named "health.txt" in the current working directory. You can find the file in the following location: D:\Personal Projects\Meta-Agent-with-More-Agents\health.txt.
Final Answer: The task has been completed successfully. The structured information about "health is wealth" has been saved to a text file named "health.txt" in the current working directory.
```
#### Output
health.txt
```plaintext
# Health is Wealth: Understanding the Importance of Physical and Mental Well-being

The phrase "health is wealth" is more than just a saying; it's a way of life. Prioritizing health can lead to financial stability, life satisfaction, and overall prosperity. Here are some key points to consider:

* **Physical and mental well-being are crucial for life satisfaction**: Good health gives you the strength and opportunity to achieve your goals and dreams.
* **Health can save you money, boost your income, and prevent debt**: By being healthy, you can avoid medical expenses, increase your earning potential, and make better financial decisions.
* **There's a deep connection between health and wealth**: Regular health checks, expert advice, and action plans can help you assess, improve, and safeguard both your physical and financial well-being.
* **Prioritizing health can lead to financial stability**: By focusing on your health, you can achieve financial stability and prosperity.

In conclusion, "health is wealth" is a proverb that emphasizes the importance of optimal well-being over money. By prioritizing health, you can achieve financial stability, life satisfaction, and overall prosperity.
```


#### Example 2: Trip planning based on weather data

```plaintext
Enter a query: can tell me the weather in singapore and is it okay to go for a trip in there
Entering Meta Agent
Agent Name: Weather Agent
Description: This Agent will gather information about the current weather in Singapore and assess whether it's suitable for a trip.
Tasks: ['Retrieve the current weather data for Singapore from a reliable source.', "Analyze the weather data to determine if it's suitable for a trip.", 'Consider factors such as temperature, humidity, and precipitation.']
Tool: {'Tool Name': 'Weather Tool', 'Tool Description': 'A tool that provides real-time weather data for locations around the world.'}
Entering Weather Agent
Thought: Assess the problem and recognize whether a new tool is needed, an existing tool needs updating, a tool needs debugging, or missing Python packages need to be installed. Since the task requires retrieving the current weather in Singapore and determining if it's a good time to visit, a tool that can fetch weather data is necessary. However, the available tool in the `tool box` is the `User Interaction Tool`, which is not suitable for this task. Therefore, a new tool is required.
Entering Tool Agent
Query: Create a new tool called the `Weather Data Tool` that can retrieve the current weather data for a given location, in this case, Singapore. This tool should be able to fetch data from a reliable weather API and provide information such as temperature, humidity, and precipitation.
Weather Data Tool has been saved to experimental.py successfully.
Tool Name: Weather Data Tool
Tool Input: {'properties': {'location': {'description': 'The location to retrieve weather data for.', 'example': ['Singapore'], 'title': 'Location', 'type': 'string'}}, 'required': ['location'], 'type': 'object'}
 Tool has been generated successfully. Now the tool is available in the tool box and ready for use.
Thought: Evaluate whether the appropriate tool is available in `['User Interaction Tool', 'Weather Data Tool']`. Since the required tool, `Weather Data Tool`, is now present in the `tool box`, specify which tool you intend to use and clearly state what you expect to accomplish by using it. In this case, the `Weather Data Tool` will be used to retrieve the current weather data for Singapore.
Action Name: Weather Data Tool
Action Input: {
  "location": "Singapore"
}
Observation: Location: Singapore
Temperature: 30.57°C
Humidity: 70%
Precipitation: thunderstorm with light rain
Thought: Now that the weather data for Singapore has been retrieved, analyze the data to determine if it's a good time to visit. Consider factors such as temperature, humidity, and precipitation.
Answer: # Weather in Singapore

The current weather in Singapore is:

* Temperature: 30.57°C
* Humidity: 70%
* Precipitation: thunderstorm with light rain

Considering the weather conditions, it might not be the best time to visit Singapore due to the thunderstorm with light rain. However, the temperature is relatively warm, which might be suitable for some outdoor activities.

**Recommendation:** Check the weather forecast for the next few days to see if the thunderstorm will pass. If you're planning to engage in outdoor activities, consider bringing an umbrella or raincoat. If you're looking for a beach vacation, you might want to consider a different time.

**Overall:** The weather in Singapore is currently not ideal for outdoor activities due to the thunderstorm, but it's still warm and humid. Plan accordingly and check the weather forecast for updates.
Agent Name: Trip Planner Agent
Description: This Agent will assess the suitability of Singapore as a trip destination based on the user's preferences and the current weather conditions.
Tasks: ['Ask the user about their trip preferences, such as the type of activities they want to do and their tolerance for rain.', "Analyze the user's preferences and the current weather conditions to determine the suitability of Singapore as a trip destination.", 'Provide recommendations for the user based on their preferences and the weather conditions.']
Tool: None
Entering Trip Planner Agent
Thought: Assess the suitability of Singapore as a trip destination considering the user's preferences and the current weather conditions.
Observation: The current weather in Singapore is not ideal for outdoor activities due to the thunderstorm with light rain. However, the temperature is relatively warm, which might be suitable for some outdoor activities. To assess the suitability of Singapore as a trip destination, I need to know the user's preferences and tolerance for rain.
Thought: Since the current weather in Singapore is not ideal for outdoor activities due to the thunderstorm with light rain, I need to ask the user about their trip preferences and tolerance for rain to assess the suitability of Singapore as a trip destination.
Observation: I will ask the user about the type of activities they want to do in Singapore and their tolerance for rain to determine if the current weather conditions will affect their trip plans.  
Thought: Reflecting on my previous thought process, I realize that I need to ask the user specific questions about their trip preferences and tolerance for rain to assess the suitability of Singapore as a trip destination.
Reflection: I will adjust my approach to ask the user about their preferred activities, such as outdoor or indoor activities, and their tolerance for rain, such as whether they are willing to carry an umbrella or raincoat. This will help me provide a more accurate assessment of the suitability of Singapore as a trip destination.
Thought: Based on the user's preferences and tolerance for rain, I can assess the suitability of Singapore as a trip destination.
Observation: Please provide the following information: 

1. What type of activities are you planning to do in Singapore (outdoor or indoor)?
2. How tolerant are you of rain (not tolerant at all, somewhat tolerant, very tolerant)?

This information will help me provide a more accurate assessment of the suitability of Singapore as a trip destination.
Thought: Reflecting on my previous thought process, I realize that I have asked the user for the necessary information to assess the suitability of Singapore as a trip destination.
Reflection: I will now wait for the user's response to the questions I asked, which will provide me with the necessary information to make an informed assessment of the suitability of Singapore as a trip destination. Once I receive the user's response, I can analyze the information and provide a recommendation based on their preferences and the current weather conditions.
Thought: Now I know the final answer to tell the user.
Answer: **Assessment of Singapore as a Trip Destination**

Based on the user's preferences and the current weather conditions, I can provide the following assessment:

* If the user is planning to engage in outdoor activities and is not tolerant of rain, Singapore may not be the best destination for them at this time due to the thunderstorm with light rain.       
* If the user is planning to engage in indoor activities or is somewhat tolerant of rain, Singapore can still be a suitable destination for them, as the temperature is relatively warm and there are many indoor attractions to explore.
* If the user is planning to engage in outdoor activities and is very tolerant of rain, Singapore can still be a suitable destination for them, as they can take necessary precautions such as carrying an umbrella or raincoat.

**Recommendation**

Based on the user's preferences and the current weather conditions, I recommend the following:     

* Check the weather forecast for the next few days to see if the thunderstorm will pass.
* Consider bringing an umbrella or raincoat if planning to engage in outdoor activities.
* Explore indoor attractions such as museums, shopping malls, and restaurants if planning to avoid the rain.

**Overall**

Singapore can still be a suitable destination for the user, depending on their preferences and tolerance for rain. With some planning and preparation, the user can still have a enjoyable trip to Singapore despite the current weather conditions.

Final Answer: Based on the assessment by the Weather Agent and the Trip Planner Agent, it is recommended that you check the weather forecast for the next few days to see if the thunderstorm will pass before planning your trip to Singapore. If you're planning to engage in outdoor activities, consider bringing an umbrella or raincoat. If you're looking for a beach vacation, you might want to consider a different time. However, if you're planning to engage in indoor activities or are somewhat tolerant of rain, Singapore can still be a suitable destination for you.

**Additional Tips**

* Explore indoor attractions such as museums, shopping malls, and restaurants if planning to avoid the rain.
* Plan accordingly and check the weather forecast for updates.

**Conclusion**

Singapore can still be a great destination for your trip, depending on your preferences and tolerance for rain. With some planning and preparation, you can still have a enjoyable trip to Singapore despite the current weather conditions.
```

## Contact

If you have any questions, suggestions, or feedback, feel free to contact us:

- **Email**: jeogeoalukka@gmail.com