# Recursion-of-Thought:
The repository contains the code used to test Recursion of Thought prompting technique as a potential solution for our problem statement

OpenAI api keys are stored in the `openai.txt` file. You can use your own OpenAI api key by modifying the file
List of all available important tools and arguments are stored in `functions.txt`. If you want to add your own new functions you can add it by editing the file.

# Methadology
Recursion of Thought is an approach in problem-solving that involves breaking down complex tasks into smaller subproblems and recursively solving them to derive the final solution.

# Local setup (Installing dependancies)
 `pip install -r requirements.txt`

# Run the following command to answer your query
 To ask your own custom query, write your custom query within quotes in the --query field
 ```
python Recursion_of_Thought.py \
--query "Retrieve work items associated with the Rev organization Rev-789 and tickets that need a response, and create a summary." \
```

# Sample result:
1.Divide the problem into subproblems:

Subproblem 1: Retrieve work items associated with the Rev organisation 'Rev-789'.

Subproblem 2: Filter work items from Subproblem 1 which are tickets that need a response.

Subproblem 3: Summarize the work items obtained from Subproblem 2.


2.Generate GO and STOP tokens:

GO

... Subproblem 1 ...

... Subproblem 2 ...

... Subproblem 3 ...

STOP


3.Solve each subproblem recursively:


For Subproblem 1, use the "works_list" tool with the argument "ticket.rev_org" set to "Rev-789".

For Subproblem 2, use the "works_list" tool with the argument "ticket.needs_response" set to true and "objects" set to the output of Subproblem 1.

Subproblem 3 does not require further division and can be solved directly using the "summarize_objects" tool with the argument "objects" set to the output of Subproblem 2.


4.Use appropriate tools and combine the outputs of Subproblems 1, 2, and 3.Replace the corresponding THINK tokens with the actual results obtained from each subproblem.

The final answer is the prioritized list of work items associated with 'Rev-789,' which are tickets that need a response, and summarized.

```
[
    {
        ""tool_name"": ""works_list"",
        ""arguments"": [
            {
                ""argument_name"": ""ticket.rev_org"",
                ""argument_value"": ""Rev-789""
            }
        ]
    },
    {
        ""tool_name"": ""works_list"",
        ""arguments"": [
            {
                ""argument_name"": ""ticket.needs_response"",
                ""argument_value"": true
            },
            {
                ""argument_name"": ""objects"",
                ""argument_value"": ""$$PREV[0]""
            }
        ]
    },
    {
        ""tool_name"": ""summarize_objects"",
        ""arguments"": [
            {
                ""argument_name"": ""objects"",
                ""argument_value"": ""$$PREV[1]""
            }
        ]
    }
]
```

# Bibliography
[Source Paper](https://arxiv.org/abs/2306.06891)
