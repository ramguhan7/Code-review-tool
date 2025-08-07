import sys
from sql_review_tool.sql_review import review_directory

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else input("Enter SQL folder: ").strip()
    report = review_directory(folder)

    has_error = False

    if not report:
        print("✅ All SQL files passed!")
    else:
        print("🧪 Review Results:")
        for file, issues in report.items():
            print(f"\n📄 {file}")
            for severity, message in issues:
                if severity == "error":
                    print(f"  ❌ {message}")
                    has_error = True
                elif severity == "warning":
                    print(f"  ⚠️  {message}")
    
    if has_error:
        print("\n❌ Failing the check due to errors.")
        exit(1)
    else:
        print("\n✅ Only warnings or no issues. Passing.")
        exit(0)
