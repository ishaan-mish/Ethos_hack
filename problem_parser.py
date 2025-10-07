import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure NLTK resources are available
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))


class ProblemParser:
    def __init__(self, topic, problem_statement):
        self.topic = topic.lower()
        self.problem_statement = problem_statement.lower()

    def parse(self):
        if "planning" in self.topic or "optimization" in self.topic:
            return self._parse_planning_problem()
        elif "spatial" in self.topic:
            return self._parse_spatial_problem()
        else:
            return self._parse_generic_problem()

    # --------------------- Planning Parser ---------------------
    def _parse_planning_problem(self):
        tasks = {}
        constraints = {}
        entities = []

        # Match main actions with durations
        matches = re.findall(
            r"([a-z\s]*?\b(?:bake|decorate|pick up|prepare|cook|clean|wash|organize|go|visit|travel)[a-z\s]*)\s+(?:which takes|that takes)\s+([0-9\.]+)\s?(hours|hour|minutes|minute)",
            self.problem_statement
        )

        for match in matches:
            task_name = "_".join([t for t in match[0].strip().split() if t not in stop_words])
            duration = float(match[1])
            if "minute" in match[2]:
                duration = duration / 60
            tasks[task_name] = {"duration": duration, "depends_on": [], "can_overlap": []}
            entities.append(task_name)

        # Detect overlapping tasks using "while X" pattern
        overlap_matches = re.findall(
            r"while ([a-z\s]*?\b(?:bake|decorate|prepare|cook|clean|wash|organize|go|visit|travel)[a-z\s]*)",
            self.problem_statement
        )
        for overlap_task in overlap_matches:
            overlap_task_name = "_".join([t for t in overlap_task.strip().split() if t not in stop_words])
            for t in tasks:
                if t != overlap_task_name:
                    tasks[t]["can_overlap"].append(overlap_task_name)

        # Detect constraints: "cannot leave for X"
        cannot_leave_match = re.findall(r"cannot leave for ([a-z\s]+?)\b", self.problem_statement)
        if cannot_leave_match:
            constraints["cannot_leave_oven"] = [
                "_".join([t for t in x.strip().split() if t not in stop_words])
                for x in cannot_leave_match
            ]

        return {
            "entities": entities,
            "actions": tasks,
            "constraints": constraints,
            "goal": "minimize total time"
        }

    # --------------------- Spatial Parser ---------------------
    def _parse_spatial_problem(self):
        entities = []
        actions = {}
        constraints = {}

        # Detect corners (lowercase or uppercase)
        points = re.findall(r"corner\s([a-z])", self.problem_statement, flags=re.IGNORECASE)
        entities.extend([p.upper() for p in points])

        # Distance constraints
        dist_matches = re.findall(
            r"distance from ([a-z]) to ([a-z\s]+?) must be (.+?)(?:\.|,|$)",
            self.problem_statement, flags=re.IGNORECASE
        )
        for m in dist_matches:
            from_point = m[0].upper()
            to_entity = m[1].strip().replace(" ", "_")
            cond = m[2].strip()
            constraints[f"{from_point}_to_{to_entity}"] = cond

        # Equidistant corners
        equidistant_matches = re.findall(
            r"equidistant from corners ([a-z](?:,\s*[a-z])*)",
            self.problem_statement, flags=re.IGNORECASE
        )
        for match in equidistant_matches:
            corners = [c.strip().upper() for c in match.split(",")]
            constraints["equidistant_corners"] = list(dict.fromkeys(corners))  # remove duplicates

        return {
            "entities": list(set(entities)),
            "actions": actions,
            "constraints": constraints,
            "goal": "find valid spatial configuration"
        }

    # --------------------- Generic Parser ---------------------
    def _parse_generic_problem(self):
        tokens = word_tokenize(self.problem_statement)
        tokens = [t.lower() for t in tokens if t.isalpha() and t.lower() not in stop_words]

        numbers = re.findall(r"\d+\.?\d*", self.problem_statement)
        logic_words = ["all", "some", "none", "more than", "less than", "if", "then", "and", "or", "not"]
        keywords = [kw for kw in logic_words if kw in self.problem_statement]

        entities = list(set(tokens))

        return {
            "entities": entities,
            "numbers": numbers,
            "keywords": keywords,
            "actions": {},
            "constraints": {},
            "goal": "solve logically"
        }
