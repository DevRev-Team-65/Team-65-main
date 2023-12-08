from openai import OpenAI
import openai
import argparse

# COT PROMPTING

parser = argparse.ArgumentParser()
parser.add_argument("--query", default=None, type=str, required=True, help="Enter your query: ")
parser.add_argument("--api_key", default=None, type=str, required=True, help="Enter your OpenAI API key: ")
args = parser.parse_args()

client = OpenAI(api_key=args.api_key)

prompt = """ You are a helpful chatbot and you need to answer the given query by giving an output in JSON format of the tools, argument names, argument values which are needed to solve the query.If the query cannot be solved by the list of tools I provide then outout an empty list.
The following is the list of tools,argument names,descriptions,examples etc. Understand the functionality of each tool and argument:
[{"tool_name":"works_list",
 "Description":"Returns a list of work items matching the request",
 "ArgumentName":"applies_to_part",
 "ArgumentDescription":"Filters for work belonging to any of the provided parts",
 "ArgumentType":"array of strings",
 "ArgumentValueExample":"Example:["FEAT-123","ENH-123","PROD-123","CAPL-123"]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"created_by",
  "ArgumentDescription":"Filters for work created by any of these users",
  "ArgumentType":"array of strings",
   "ArgumentValueExample":"Example:["DEVU-123"]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"issue.priority",
  "ArgumentDescription":"Filters for issues with any of the provided priorities. Allowed values: p0, p1, p2,p3",
  "ArgumentType":"array of strings",
  "ArgumentValueExample":"[]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"issue.rev_orgs",
  "ArgumentDescription":"Filters for issues with any of the provided Rev organizations",
  "ArgumentType":"array of strings",
  "ArgumentValueExample":"Example:["REV-123""},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"limit",
  "ArgumentDescription":"The maximum number of works to return. The default is'50'",
  "ArgumentType":"integer (int32)",
 "ArgumentValueExample":"[]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"owned_by",
  "ArgumentDescription":"Filters for work owned by any of these users",
  "ArgumentType":"array of strings",
  "ArgumentValueExample":"Example:["DEVU-123"]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"stage.name",
  "ArgumentDescription":"Filters for records in the provided stage(s) by name",
  "ArgumentType":"array of strings",
  "ArgumentValueExample":"[]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"ticket.needs_response",
  "ArgumentDescription":"Filters for tickets that need a response",
  "ArgumentType":"boolean",
  "ArgumentValueExample":"[]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"ticket.rev_org",
  "ArgumentDescription":"Filters for tickets associated with any of the provided Rev organizations",
  "ArgumentType":"array of strings",
  "ArgumentValueExample":"Example:["REV-123"]"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"ticket.severity",
  "ArgumentDescription":"Filters for tickets with any of the provided severities. Allowed values: blocker, high, low, medium"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"ticket.source_channel",
  "ArgumentDescription":"Filters for tickets with any of the provided source channels",
  "ArgumentType":"array of strings"},
 {"tool_name":"works_list",
  "Description":"Returns a list of work items matching the request",
  "ArgumentName":"type",
  "ArgumentDescription":"Filters for work of the provided types. Allowed values: issue, ticket, task",
  "ArgumentType":"array of strings"},
 {"tool_name":"summarize_objects",
  "Description":"Summarizes a list of objects. The logic of how to summarize a particular object type is an internal implementation detail.",
  "ArgumentName":"objects",
  "ArgumentDescription":"List of objects to summarize",
  "ArgumentType":"array of objects"},
 {"tool_name":"prioritize_objects",
  "Description":"Returns a list of objects sorted by priority. The logic of what constitutes priority for a given object is an internal implementation detail.",
  "ArgumentName":"objects",
  "ArgumentDescription":"A list of objects to be prioritized",
  "ArgumentType":"array of objects"},
 {"tool_name":"add_work_items_to_sprint",
  "Description":"Adds the given work items to the sprint",
  "ArgumentName":"work_ids",
  "ArgumentDescription":"A list of work item IDs to be added to the sprint",
  "ArgumentType":"array of objects"},
 {"tool_name":"add_work_items_to_sprint",
  "Description":"Adds the given work items to the sprint",
  "ArgumentName":"sprint_id",
  "ArgumentDescription":"The ID of the sprint to which the work items should be added",
  "ArgumentType":"str"},
 {"tool_name":"get_sprint_id",
  "Description":"Returns the ID of the current sprint"},
 {"tool_name":"get_similar_work_item",
  "Description":"Returns a list of work items that are similar to the given work item",
  "ArgumentName":"work_id ",
  "ArgumentDescription":"The ID of the work item for which you want to find similar items",
  "ArgumentType":"string"},
 {"tool_name":"search_object_by_name",
  "Description":"Given a search string, returns the id of a matching object in the system of record. If multiple matches are found, it returns the one where the confidence is highest.",
  "ArgumentName":"query",
  "ArgumentDescription":"The search string, could be for example customer’s name, part name, user name.",
  "ArgumentType":"string"},
 {"tool_name":"create_actionable_tasks_from_text",
  "Description":"Given a text, extracts actionable insights, and creates tasks for them, which are kind of a work item.",
  "ArgumentName":"text",
  "ArgumentDescription":"The text from which the actionable insights need to be created.",
  "ArgumentType":"string"},
 {"tool_name":"who_am_i",
  "Description":"Returns the ID of the current user"}]


To reference the value of the ith tool in the chain, use $$PREV[i] as argument value. i =
0, 1, .. j-1; j = current tool’s index in the array
If the query could not be answered with the given set of tools, output an empty list instead.


  Sample queries and their outputs:
  [{"Query":"Summarize issues similar to don:core:dvrv-us-1:devo/0:issue/1"},
"Output":[
{
"tool_name": "get_similar_work_items",
"arguments": [
{
"argument_name": "work_id",
"argument_value": "don:core:dvrv-us-1:devo/0:issue/1"
}
]
},
{
"tool_name": "summarize_objects",
"arguments": [
{
"argument_name": "objects",
"argument_value": "$$PREV[0]"
}
]
}
],
{"Query":"What is the meaning of life?",
"Output":[]},
{"Query":"Prioritize my P0 issues and add them to the current sprint",
"Output":[
{
"tool_name": "whoami",
"arguments": []
},
{
"tool_name": "works_list",
"arguments": [
{
"argument_name": "issue.priority",
"argument_value": "p0"
},
{
"argument_name": "owned_by",
"argument_value": "$$PREV[0]"
}
]
},
{
"tool_name": "prioritize_objects",
"arguments": [
{
"argument_name": "objects",
"argument_value": "$$PREV[1]"
}
]
},
{
"tool_name": "get_sprint_id",
"arguments": []
},
{
"tool_name": "add_work_items_to_sprint",
"arguments": [
{
"argument_name": "work_ids",
"argument_value": "$$PREV[2]"
},
{
"argument_name": "sprint_id",
"argument_value": "$$PREV[3]"
}
]
}
]},
{"Query":"Summarize high severity tickets from the customer UltimateCustomer",
"Output":
{
"tool_name": "search_object_by_name",
"arguments": [
{
"argument_name": "query",
"argument_value": "UltimateCustomer"
}
]
},
{
"tool_name": "works_list",
"arguments": [
{
"argument_name": "ticket.rev_org",
"argument_value": "$$PREV[0]"
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
]},
{"Query":"What are my all issues in the triage stage under part FEAT-123? Summarize them.",
"Output":[
{
"tool_name": "whoami",
"arguments": []
},
{
"tool_name": "works_list",
"arguments": [
{
"argument_name": "stage.name",
"argument_value": "triage"
},
{
"argument_name": "applies_to_part",
"argument_value": "FEAT-123"
},
{
"argument_name": "owned_by",
"argument_value": "$$PREV[0]"
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
]},
{"Query":"List all high severity tickets coming in from slack from customer Cust123 and generate a summary of them.",
"Output":[
{
"tool_name": "search_object_by_name",
"arguments": [
{
"argument_name": "query",
"argument_value": "Cust123"
}
]
},
{
"tool_name": "works_list",
"arguments": [
{
"argument_name": "ticket.rev_org",
"argument_value": "$$PREV[0]"
},
{
"argument_name": "ticket.severity",
"argument_value": "high"
},
{
"argument_name": "ticket.source_channel",
"argument_value": "slack"
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
]},
{"Query":"Given a customer meeting transcript T, create action items and add them to my current sprint",
"Output":[
{
"tool_name": "create_actionable_tasks_from_text",
"arguments": [
{
"argument_name": "text",
"argument_value": "T"
}
]
},
{
"tool_name": "get_sprint_id",
"arguments": []
},
{
"tool_name": "add_work_items_to_sprint",
"arguments": [
{
"argument_name": "work_ids",
"argument_value": "$$PREV[0]"
},
{
"argument_name": "sprint_id",
"argument_value": "$$PREV[1]"
}
]
}
]},
{"Query":"Get all work items similar to TKT-123, summarize them, create issues from that summary, and prioritize them",
"Output":[
{
"tool_name": "get_similar_work_items",
"arguments": [
{
"argument_name": "work_id",
"argument_value": "TKT-123"
}
]
},
{
"tool_name": "create_actionable_tasks_from_text",
"arguments": [
{
"argument_name": "text",
"argument_value": "$$PREV[0]"
}
]
},
{
"tool_name": "prioritize_objects",
"arguments": [
{
"argument_name": "objects",
"argument_value": "$$PREV[1]"
}
]
}
]
}]
The output is in JSON format.

When given a query you should first think what you should do.
E.g if the query is "Retrieve work items associated with the Rev organisation 'REV-123' and owned by the user 'DEVU-789'" then the thought process should be:
Based on the given query, my thought process for solving it would be as follows:
- We need to retrieve work items associated with a specific Rev organisation  and owned by a specific user
- Since we need to filter for work items, the 'works_list' tool would be useful.
- Looking at the available arguments for `worklist`, we can see that the `ticket.rev_org` and `owned_by` arguments are relevant to the query.
- Therefore, we can use the `ticket.rev_org` argument with the value of "REV-123" and the `owned_by` argument with the value of "DEVU-789".
- The desired output format is in json, so we can create a list of objects (tools) and their respective arguments and values in json format.
- The first object would be the `works_list` tool with the arguments for `ticket.rev_org` and `owned_by` and their corresponding values.
- The second object would be the `summarize_objects` tool with the argument for `objects` and the value of "REV-123" from the `works_list` tool.
- The final output would then be in the form of a list of json objects with the tool name and its arguments and values, as follows:
[{
  "tool_name": "works_list",
  "arguments": [
    {
      "argument_name": "ticket.rev_org",
      "argument_value": "REV-123"
    },
    {
      "argument_name": "owned_by",
      "argument_value": "DEVU-789"
    }
  ]
},
{
  "tool_name": "summarize_objects",
  "arguments": [
    {
      "argument_name": "objects",
      "argument_value": "$$PREV[0]"
    }
  ]
}]

if the query is "Summarize issues similar to
don:core:dvrv-us-1:devo/0:issue/1" then the thought process should be:
  I have to summarize issues similar to "don:core:dvrv-us-1:devo/0:issue/1. So I should use the tool "get_similar_work_items" and argument"work_id" and the argument value can be don:core:dvrv-us-1:devo/0:issue/1. I also have to summarize so I should use the tool  "summarize_objects" and argument name  "objects".

  Understand well the functionalities of the tools and arguments and output in JSON format the tool name, argument name, argument value etc which are needed to solve the following query:"""

add = f"{args.query}. Give the output in JSON format which includes all the tools and arguments necessary to answer the query and also show your thought process for this query. Refer to the sample queries and the outputs I had given."
tup = (prompt,add)
prompt_final = ' '.join(tup)

response = client.completions.create(
  model="gpt-3.5-turbo-instruct",
  prompt=prompt_final,
  max_tokens = 1000  
)
print(response.choices[0].text)
