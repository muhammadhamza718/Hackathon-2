import os
import shutil
from pathlib import Path

# Base directory
base_dir = Path(r"f:\Courses\Hamza\Hackathon-2-Phase-1")

# Phases to clean
phases = ["Phase-2", "Phase-3", "Phase-4", "Phase-5"]

print("="*60)
print("Removing Old (auth) Directories")
print("="*60)

for phase in phases:
    old_auth_dir = base_dir / phase / "frontend" / "app" / "(auth)"
    
    if old_auth_dir.exists():
        try:
            print(f"\n{phase}: Removing {old_auth_dir}")
            shutil.rmtree(old_auth_dir)
            print(f"✅ {phase}: Successfully deleted (auth) directory")
        except Exception as e:
            print(f"❌ {phase}: Error deleting directory: {e}")
    else:
        print(f"✅ {phase}: (auth) directory already removed")

print("\n" + "="*60)
print("Verification")
print("="*60)

for phase in phases:
    old_auth_dir = base_dir / phase / "frontend" / "app" / "(auth)"
    new_auth_dir = base_dir / phase / "frontend" / "app" / "auth"
    
    old_exists = "❌ STILL EXISTS" if old_auth_dir.exists() else "✅ DELETED"
    new_exists = "✅ EXISTS" if new_auth_dir.exists() else "❌ MISSING"
    
    print(f"\n{phase}:")
    print(f"  Old (auth): {old_exists}")
    print(f"  New auth:   {new_exists}")

print("\n" + "="*60)
print("✅ Cleanup Complete!")
print("="*60)
