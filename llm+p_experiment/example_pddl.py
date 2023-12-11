problem = '''I want you to solve planning problems. An example planning problem is: 
Prioritize my P0 issues and add them to the current sprint. 
'''
pddl_solution = '''
The problem PDDL file to this problem is: 
(define (domain tool_domain)
  (:requirements :strips :typing)
  (:types tool object)
  (:predicates
    (tool_used ?t - tool)
    (argument_of ?a - tool ?arg - object)
    (tool_argument_value ?arg - object)
    (previous_result ?prev - object)
  )

  ;; Actions
  (:action use_tool_whoami
    :parameters ()
    :precondition (and)
    :effect (and
      (tool_used whoami)
      (argument_of whoami)
    )
  )

  (:action use_tool_works_list
    :parameters ()
    :precondition (and
      (tool_used whoami)
      (argument_of whoami)
    )
    :effect (and
      (tool_used works_list)
      (argument_of works_list (issue.priority p0) (owned_by ?prev))
      (previous_result ?prev)
    )
  )

  (:action use_tool_prioritize_objects
    :parameters ()
    :precondition (and
      (tool_used works_list)
      (argument_of works_list (issue.priority p0) (owned_by ?prev))
      (previous_result ?prev)
    )
    :effect (and
      (tool_used prioritize_objects)
      (argument_of prioritize_objects (objects ?prev))
      (previous_result ?prev)
    )
  )

  (:action use_tool_get_sprint_id
    :parameters ()
    :precondition (and)
    :effect (and
      (tool_used get_sprint_id)
      (argument_of get_sprint_id)
    )
  )

  (:action use_tool_add_work_items_to_sprint
    :parameters ()
    :precondition (and
      (tool_used prioritize_objects)
      (argument_of prioritize_objects (objects ?prev))
      (tool_used get_sprint_id)
      (argument_of get_sprint_id)
    )
    :effect (and
      (tool_used add_work_items_to_sprint)
      (argument_of add_work_items_to_sprint (work_ids ?prev) (sprint_id ?prev))
      (previous_result ?prev)
    )
  )
)

'''