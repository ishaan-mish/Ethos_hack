from typing import Dict, List, Any

class ProblemDecomposer:
    def __init__(self, structured_problem: Dict[str, Any]):
        self.problem = structured_problem
        self.actions = structured_problem.get("actions", {})
        self.constraints = structured_problem.get("constraints", {})
        self.entities = structured_problem.get("entities", [])
        self.goal = structured_problem.get("goal", "")

    def decompose(self) -> List[Dict[str, Any]]:
        subtask_plan = []

        for task_name, task_info in self.actions.items():
            subtask = {
                "task": task_name,
                "duration": task_info.get("duration", 0),
                "depends_on": task_info.get("depends_on", []),
                "can_overlap": task_info.get("can_overlap", []),
                "constraints": []
            }

            # Apply constraints from 'cannot_leave_oven' or others
            for c_key, c_tasks in self.constraints.items():
                if task_name in c_tasks:
                    subtask["constraints"].append(c_key)

            subtask_plan.append(subtask)

        # Resolve dependencies implied by constraints
        subtask_plan = self._apply_dependency_constraints(subtask_plan)

        return subtask_plan

    def _apply_dependency_constraints(self, plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Example: If a task cannot be done before another task (cannot_leave_oven),
        automatically add the dependency.
        """
        task_names = {t["task"] for t in plan}

        for task in plan:
            for constraint in task.get("constraints", []):
                if constraint == "cannot_leave_oven":
                    # Assume 'cannot_leave_oven' means must wait for all other tasks baking first
                    for other_task in plan:
                        if other_task["task"] != task["task"] and "bake" in other_task["task"]:
                            if other_task["task"] not in task["depends_on"]:
                                task["depends_on"].append(other_task["task"])

        return plan
