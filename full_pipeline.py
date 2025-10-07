# full_pipeline.py
import json
from dataset_loader import DatasetLoader
from problem_parser import ProblemParser
from problem_decomposer import ProblemDecomposer
from tool_selector import ToolAssigner

def main():
    # Step 1: Load dataset
    file_path = r"C:\Users\ishaa\Downloads\ML Challenge Dataset-20251007T191245Z-1-001\ML Challenge Dataset\train.csv"
    loader = DatasetLoader(file_path)
    dataset = loader.load()
    
    full_parsed_dataset = []

    for idx, sample in enumerate(dataset):
        topic = sample["topic"]
        statement = sample["problem_statement"]
        
        # Step 2: Parse problem
        parser = ProblemParser(topic, statement)
        parsed = parser.parse()
        
        # Step 3: Decompose problem into subtasks
        decomposer = ProblemDecomposer(parsed)
        subtasks = decomposer.decompose()
        
        # Step 4: Assign appropriate tools
        assigner = ToolAssigner(topic, parsed, subtasks)
        tool_assigned_subtasks = assigner.assign_tools()
        
        # Combine everything
        full_entry = {
            "topic": topic,
            "original_problem": statement,
            "parsed_problem": parsed,
            "subtasks": subtasks,
            "subtasks_with_tools": tool_assigned_subtasks,
            "solution": sample.get("solution", ""),
            "answer_options": [
                sample.get("answer_option_1", ""),
                sample.get("answer_option_2", ""),
                sample.get("answer_option_3", ""),
                sample.get("answer_option_4", ""),
                sample.get("answer_option_5", "")
            ],
            "correct_option_number": sample.get("correct_option_number", None)
        }
        full_parsed_dataset.append(full_entry)
        
    # Save to JSON
    with open("parsed_dataset_with_tools.json", "w", encoding="utf-8") as f:
        json.dump(full_parsed_dataset, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Processed {len(dataset)} problems and saved to parsed_dataset_with_tools.json")

if __name__ == "__main__":
    main()
