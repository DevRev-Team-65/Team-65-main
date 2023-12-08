example_queries = [
    (
        "Summarize issues similar to don:core:dvrv-us-1:devo/0:issue/1",
        """[
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
        ]"""
    ),
    (
        "What is the meaning of life?",
        "[]"
    ),
    (
        "Prioritize my P0 issues and add them to the current sprint",
        """[
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
        ]"""
    ),
    (
        "Summarize high severity tickets from the customer UltimateCustomer",
        """[
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
        ]"""
    ),
    (
        "What are my all issues in the triage stage under part FEAT-123? Summarize them.",
        """[
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
        ]"""
    ),
    (
        "List all high severity tickets coming in from slack from customer Cust123 and generate a summary of them.",
        """[
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
        ]"""
    ),
    (
        "Given a customer meeting transcript T, create action items and add them to my current sprint",
        """[
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
        ]"""
    ),
    (
        "Get all work items similar to TKT-123, summarize them, create issues from that summary, and prioritize them",
        """[
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
        ]"""
    )
]