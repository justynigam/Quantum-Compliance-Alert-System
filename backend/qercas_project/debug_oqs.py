import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Python version:", sys.version)
print("Python path:", sys.path[:3])  # Show first 3 entries

try:
    import oqs
    print("\n✓ Successfully imported oqs")
    print("OQS module file:", oqs.__file__)
    print("OQS module dict keys:", list(oqs.__dict__.keys())[:10])  # First 10 keys
    
    print("\nAll available attributes in oqs:")
    for attr in sorted(dir(oqs)):
        if not attr.startswith('_'):
            try:
                obj = getattr(oqs, attr)
                print(f"  {attr}: {type(obj).__name__}")
            except Exception as e:
                print(f"  {attr}: Error accessing - {e}")
                
    # Check for common class names
    classes_to_check = ['KeyEncapsulation', 'KEM', 'Kem', 'keyencapsulation']
    print(f"\nChecking for common class names:")
    for cls_name in classes_to_check:
        if hasattr(oqs, cls_name):
            print(f"  ✓ Found: oqs.{cls_name}")
        else:
            print(f"  ✗ Not found: oqs.{cls_name}")
            
    # Check for functions
    functions_to_check = ['get_enabled_kem_mechanisms', 'get_enabled_KEM_mechanisms']
    print(f"\nChecking for functions:")
    for func_name in functions_to_check:
        if hasattr(oqs, func_name):
            print(f"  ✓ Found: oqs.{func_name}")
            try:
                result = getattr(oqs, func_name)()
                print(f"    Available algorithms: {result[:3]}...")  # First 3
            except Exception as e:
                print(f"    Error calling: {e}")
        else:
            print(f"  ✗ Not found: oqs.{func_name}")

except ImportError as e:
    print(f"✗ Failed to import oqs: {e}")
    print("Checking if liboqs-python is installed...")
    
    try:
        import pkg_resources
        installed_packages = [d.project_name for d in pkg_resources.working_set]
        oqs_packages = [p for p in installed_packages if 'oqs' in p.lower() or 'liboqs' in p.lower()]
        print(f"OQS-related packages found: {oqs_packages}")
    except:
        print("Could not check installed packages")

except Exception as e:
    print(f"✗ Unexpected error: {e}")

print("\nDone.")
