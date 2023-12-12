DEVREV_PROMPT = '''
Q: Find all tasks related to customer ABC Inc. and summarize them.

# solution JSON:

"[
  {
    ""tool_name"": ""works_list"",
    ""arguments"": [
      {
        ""argument_name"": ""created_by"",
        ""argument_value"": [""DEVU-123"", ""DEVU-456""]
      }
    ]
  },
  {
    ""tool_name"": ""summarize_objects"",
    ""arguments"": [
      {
        ""argument_name"": ""objects"",
        ""argument_value"": ""$$PREV[0]""
      }
    ]
  }
]"

Q: Search for objects related to the customer CustomerABC and create action items from the search results.

# solution JSON:

"[
  {
    ""tool_name"": ""search_object_by_name"",
    ""arguments"": [
      {
        ""argument_name"": ""query"",
        ""argument_value"": ""CustomerABC""
      }
    ]
  },
  {
    ""tool_name"": ""create_actionable_tasks_from_text"",
    ""arguments"": [
      {
        ""argument_name"": ""text"",
        ""argument_value"": ""$$PREV[0]""
      }
    ]
  }
]"

Q:  Retrieve work items with the highest severity blocker and prioritize them.

# solution:

"[
  {
    ""tool_name"": ""works_list"",
    ""arguments"": [
      {
        ""argument_name"": ""ticket.severity"",
        ""argument_value"": ""blocker""
      }
    ]
  },
  {
    ""tool_name"": ""prioritize_objects"",
    ""arguments"": [
      {
        ""argument_name"": ""objects"",
        ""argument_value"": ""$$PREV[0]""
      }
    ]
  }
]"

Q: Find all work items in the testing stage that are related to parts PART-1 and PART-2 and summarize them.

# solution JSON:

"[
  {
    ""tool_name"": ""works_list"",
    ""arguments"": [
      {
        ""argument_name"": ""stage.name"",
        ""argument_value"": ""testing""
      },
      {
        ""argument_name"": ""applies_to_part"",
        ""argument_value"": [""PART-1"", ""PART-2""]
      }
    ]
  },
  {
    ""tool_name"": ""summarize_objects"",
    ""arguments"": [
      {
        ""argument_name"": ""objects"",
        ""argument_value"": ""$$PREV[0]""
      }
    ]
  }
]"

Q: Retrieve work items associated with the Rev organization Rev-789 and tickets that need a response, and create a summary.

# solution JSON:

"[
  {
    ""tool_name"": ""works_list"",
    ""arguments"": [
      {
        ""argument_name"": ""ticket.rev_org"",
        ""argument_value"": ""Rev-789""
      },
      {
        ""argument_name"": ""ticket.needs_response"",
        ""argument_value"": true
      }
    ]
  },
  {
    ""tool_name"": ""summarize_objects"",
    ""arguments"": [
      {
        ""argument_name"": ""objects"",
        ""argument_value"": ""$$PREV[0]""
      }
    ]
  }
]"

Q: Find work items with medium severity and owned by user USER-789, and then prioritize them.

# solution JSON:

"[
  {
    ""tool_name"": ""works_list"",
    ""arguments"": [
      {
        ""argument_name"": ""ticket.severity"",
        ""argument_value"": ""medium""
      },
      {
        ""argument_name"": ""owned_by"",
        ""argument_value"": ""USER-789""
      }
    ]
  },
  {
    ""tool_name"": ""prioritize_objects"",
    ""arguments"": [
      {
        ""argument_name"": ""objects"",
        ""argument_value"": ""$$PREV[0]""
      }
    ]
  }
]"

Q: Retrieve work items in the design stage and owned by USER-456, then create action items from the results.

# solution JSON:

"[
  {
    ""tool_name"": ""works_list"",
    ""arguments"": [
      {
        ""argument_name"": ""stage.name"",
        ""argument_value"": ""design""
      },
      {
        ""argument_name"": ""owned_by"",
        ""argument_value"": ""USER-456""
      }
    ]
  },
  {
    ""tool_name"": ""create_actionable_tasks_from_text"",
    ""arguments"": [
      {
        ""argument_name"": ""text"",
        ""argument_value"": ""$$PREV[0]""
      }
    ]
  }
]"

Q: Get the current sprint ID and then find work items in that sprint.

# solution JSON:

"[
  {
    ""tool_name"": ""get_sprint_id"",
    ""arguments"": []
  },
  {
    ""tool_name"": ""works_list"",
    ""arguments"": [
      {
        ""argument_name"": ""sprint_id"",
        ""argument_value"": ""$$PREV[0]""
      }
    ]
  }
]"

Q: Search for objects related to ProjectX and summarize them.

# solution JSON:

"[
  {
    ""tool_name"": ""search_object_by_name"",
    ""arguments"": [
      {
        ""argument_name"": ""query"",
        ""argument_value"": ""ProjectX""
      }
    ]
  },
  {
    ""tool_name"": ""summarize_objects"",
    ""arguments"": [
      {
        ""argument_name"": ""objects"",
        ""argument_value"": ""$$PREV[0]""
      }
    ]
  }
]"

Q: {question}

# solution JSON:

'''.strip() + '\n\n'