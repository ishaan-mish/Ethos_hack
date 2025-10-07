# tool_assigner.py
class ToolAssigner:
    def __init__(self, topic, parsed_problem, subtasks):
        self.topic = topic.lower()
        self.parsed_problem = parsed_problem
        self.subtasks = subtasks

    def assign_tools(self):
        assigned_subtasks = []

        if self.subtasks:
            for task in self.subtasks:
                tool = self._choose_tool(task)
                task_with_tool = task.copy()
                task_with_tool["tool"] = tool
                assigned_subtasks.append(task_with_tool)
        else:
            # For problems with no explicit subtasks
            assigned_subtasks.append({
                "task": "full_problem",
                "tool": self._choose_tool(None),
                "details": "No explicit subtasks; apply appropriate solver"
            })
        return assigned_subtasks

    def _choose_tool(self, task):
        # Fine-grained heuristics
        if "optimization" in self.topic or "planning" in self.topic:
            return "calculator"  # or "optimizer"
        elif "spatial" in self.topic or "geometry" in self.topic:
            return "symbolic_solver"
        elif "sequence" in self.topic or "riddle" in self.topic or "logical trap" in self.topic:
            return "LLM_reasoning"
        elif task and "numeric" in str(task) or "time" in str(task) or "distance" in str(task):
            return "statistical_solver"
        else:
            return "LLM_reasoning"
