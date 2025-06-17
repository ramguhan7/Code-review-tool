import sys
# ✅ NEW
from sql_review_tool.sql_review import review_directory


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else input("Enter SQL folder: ").strip()
    report = review_directory(folder)
    if not report:
        print("✅ All SQL files passed!")
    else:
        print("❌ Issues found:")
        for file, issues in report.items():
            print(f"\n{file}")
            for issue in issues:
                print(f"  - {issue}")
        exit(1)
