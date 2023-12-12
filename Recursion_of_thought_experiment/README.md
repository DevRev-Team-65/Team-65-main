# Recursion-of-Thought:
The repository contains the code used to test Recursion of Thought prompting technique as a potential solution for our problem statement


# OpenAI integration
To access OpenAI's API, the necessary API keys are stored in the 'openai.txt' file. Users can integrate their own OpenAI API key by modifying this file.


# Tool and Argument Documentation:
The comprehensive list of essential tools and arguments is documented in the 'functions.py' file. To extend functionality, users have the flexibility to introduce new functions by editing this file.


# Methodology
Recursion of Thought is an approach in problem-solving that involves breaking down complex tasks into smaller subproblems and recursively solving them to derive the final solution.

# Local setup (Installing dependencies)
 `pip install -r requirements.txt`

# Solving the query using rot function
 Customize the query below to suit the reporting needs.
 ```
from Recursion_of_thought_experiment.Recursion_of_Thought import rot
query = "Retrieve work items associated with the Rev organization Rev-789 and tickets that need a response, and create a summary."
rot(query)
```

# Sample result:
```
1. Divide the problem into subproblems:

Subproblem 1: Retrieve work items associated with the Rev organisation 'Rev-789'.
Subproblem 2: Filter work items from Subproblem 1 to only include those that need a response.
Subproblem 3: Create a summary of the work items obtained from Subproblem 2.

2. Generate GO and STOP tokens:
GO
... Subproblem 1 ...
... Subproblem 2 ...
... Subproblem 3 ...
STOP

3. Solve each subproblem recursively:

For Subproblem 1, use the "works_list" tool with the argument "ticket.rev_org" set to "Rev-789."
For Subproblem 2, use the "works_list" tool with the argument "ticket.needs_response" set to true and "objects" set to the output of Subproblem 1.
Subproblem 3 does not require further division and can be solved directly using the "summarize_objects" tool with the argument "objects" set to the output of Subproblem 2.

4. Use appropriate tools and combine the outputs of Subproblems 1, 2, and 3. Replace the corresponding THINK tokens with the actual results obtained from each subproblem.

The final answer is the summarized list of work items associated with 'REV-789' that need a response.

json
[
  {
    "tool_name": "works_list",
    "arguments": [
      {
        "argument_name": "ticket.rev_org",
        "argument_value": "Rev-789"
      }
    ]
  },
  {
    "tool_name": "works_list",
    "arguments": [
      {
        "argument_name": "objects",
        "argument_value": "$$PREV[0]"
      },
      {
        "argument_name": "ticket.needs_response",
        "argument_value": "true"
      }
    ]
  },
  {
    "tool_name": "summarize_objects",
    "arguments": [
      {
        "argument_name": "objects",
        "argument_value": "$$PREV[1]"
      }
    ]
  }
]
```

# Analysis
The evaluation of the Recursion of Thought methodology reveals a systematic and structured problem-solving technique. The breakdown of complex tasks into manageable subproblems, as illustrated in the sample result, demonstrates a clear and effective recursive approach. The use of explicit GO and STOP tokens enhances comprehension and aids in tracking the recursive process.

# Bibliography
[Source Paper](https://arxiv.org/abs/2306.06891)
