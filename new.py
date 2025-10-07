import pandas as pd

# Load the CSV file (update the path as needed)
df = pd.read_csv(r'C:\Users\ishaa\Downloads\ML Challenge Dataset-20251007T191245Z-1-001\ML Challenge Dataset\train.csv')

# Get all unique topics
unique_topics = df['topic'].unique()

# Print them
print("List of topics in the dataset:")
for topic in unique_topics:
    print("-", topic)
