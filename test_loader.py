# test_pipeline.py
from dataset_loader import DatasetLoader
from problem_parser import ProblemParser
from problem_decomposer import ProblemDecomposer
from tool_selector import ToolSelector
import pprint

if __name__ == "__main__":
    file_path = r'C:\Users\ishaa\Downloads\ML Challenge Dataset-20251007T191245Z-1-001\ML Challenge Dataset\train.csv'
    
    # -------------------------
    # Module 1: Load Dataset
    # -------------------------
    loader = DatasetLoader(file_path)
    dataset = loader.load()
    print(f"✅ Loaded {len(dataset)} problems\n")

    # Test first 5 problems
    for idx, sample in enumerate(dataset[:5]):
        print(f"\n=== Problem {idx + 1} | Topic: {sample['topic']} ===\n")
        
        # -------------------------
        # Module 2: Parse Problem
        # -------------------------
        parser = ProblemParser(sample["topic"], sample["problem_statement"])
        parsed_problem = parser.parse()
        
        print("Original Problem Statement:\n", sample["problem_statement"])
        print("\nParsed Structured Problem:")
        pprint.pprint(parsed_problem)
        
        # -------------------------
        # Module 3: Decompose Problem
        # -------------------------
        decomposer = ProblemDecomposer(parsed_problem)
        subtask_plan = decomposer.decompose()
        
        print("\nSubtask Plan (Decomposed):")
        for task in subtask_plan:
            pprint.pprint(task)

        # -------------------------
        # Module 4: Tool Selection
        # -------------------------
        selector = ToolSelector(parsed_problem, subtask_plan)
        assigned_tools = selector.assign_tools()
        
        print("\nSubtask Plan with Assigned Tools:")
        for task in assigned_tools:
            pprint.pprint(task)

        print("\n" + "="*80 + "\n")
