from knowledge_manager import knowledge
import os
import time
import sys

# Ensure we can import the assistant modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

PROJECTS = [
    "/Users/sahajpatel/Library/Mobile Documents/com~apple~CloudDocs/Weekend Projects/ClearDoc",
    "/Users/sahajpatel/Library/Mobile Documents/com~apple~CloudDocs/Weekend Projects/voiceagent"
]

# Filtering for high-signal files only to avoid noise
EXTENSIONS = {
    '.py',
    '.md',
    '.txt',
    '.js',
    '.ts',
    '.html',
    '.css',
    '.pdf',
    '.json',
    '.yaml'}


def run_neural_bridge():
    print("--- CHRISTIN NEURAL INGESTION BRIDGE ---")
    print(f"Targeting: {len(PROJECTS)} external project arrays.")

    for project_path in PROJECTS:
        if not os.path.exists(project_path):
            print(f"[!] Warning: Project path not accessible: {project_path}")
            continue

        print(f"\n[SCANNING] {os.path.basename(project_path)}...")
        file_count = 0

        for root, dirs, files in os.walk(project_path):
            # Ignore binary/temp folders
            dirs[:] = [
                d for d in dirs if d not in {
                    'node_modules',
                    '__pycache__',
                    '.git',
                    'venv',
                    'dist',
                    'build'}]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in EXTENSIONS:
                    full_path = os.path.join(root, file)
                    try:
                        # Ingest into vector DB
                        knowledge.ingest_file(full_path)
                        file_count += 1
                        print(f"  [+] Digested: {file}")
                        # Delay to prevent rate-limiting on embedding API
                        time.sleep(0.2)
                    except Exception as e:
                        print(f"  [!] Failed {file}: {str(e)}")

        print(f"[COMPLETED] {file_count} nodes added to long-term memory.")

    print("\n--- PERFORMANCE VALIDATION ---")
    print("Testing cross-project correlation threshold...")

    # Validation Query
    test_query = "Compare the architecture of ClearDoc and voiceagent."
    result = knowledge.query_knowledge(test_query)

    if result:
        print("[RESULT] Retrieval successful. Data issemantically indexed.")
        print(f"[SAMPLE CONTEXT FOUND]:\n{result[:300]}...")
    else:
        print("[RESULT] Failure. Neural link is empty or threshold is too low.")


if __name__ == "__main__":
    run_neural_bridge()
