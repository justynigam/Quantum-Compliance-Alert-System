#!/usr/bin/env python3
"""
Test script to explore the oqs module structure and find correct API
"""

try:
    import oqs
    print("OQS module imported successfully")
    print(f"OQS module location: {oqs.__file__}")
    print(f"OQS module version: {getattr(oqs, '__version__', 'Unknown')}")
    print("\nAvailable attributes in oqs module:")
    for attr in sorted(dir(oqs)):
        if not attr.startswith('_'):
            obj = getattr(oqs, attr)
            print(f"  {attr}: {type(obj)}")
    
    # Try to find KEM-related classes
    print("\nLooking for KEM-related functionality:")
    kem_attrs = [attr for attr in dir(oqs) if 'kem' in attr.lower() or 'KEM' in attr]
    for attr in kem_attrs:
        print(f"  Found: {attr}")
    
    # Check if there are any classes that might be for key encapsulation
    print("\nChecking for classes:")
    for attr in dir(oqs):
        obj = getattr(oqs, attr)
        if isinstance(obj, type):
            print(f"  Class: {attr}")
    
    # Try common API patterns
    print("\nTesting common API patterns:")
    
    # Pattern 1: Direct KEM class
    try:
        kem = oqs.KEM("Kyber768")
        print("✓ oqs.KEM works")
    except Exception as e:
        print(f"✗ oqs.KEM failed: {e}")
    
    # Pattern 2: KeyEncapsulation class
    try:
        kem = oqs.KeyEncapsulation("Kyber768")
        print("✓ oqs.KeyEncapsulation works")
    except Exception as e:
        print(f"✗ oqs.KeyEncapsulation failed: {e}")
    
    # Pattern 3: Check if there's a submodule
    if hasattr(oqs, 'kem'):
        print("Found oqs.kem submodule")
        try:
            kem = oqs.kem.KEM("Kyber768")
            print("✓ oqs.kem.KEM works")
        except Exception as e:
            print(f"✗ oqs.kem.KEM failed: {e}")
    
    # List supported algorithms
    try:
        if hasattr(oqs, 'get_enabled_KEM_mechanisms'):
            algorithms = oqs.get_enabled_KEM_mechanisms()
            print(f"\nSupported KEM algorithms: {algorithms[:5]}...")  # Show first 5
        elif hasattr(oqs, 'enabled_KEMs'):
            algorithms = oqs.enabled_KEMs()
            print(f"\nSupported KEM algorithms: {algorithms[:5]}...")  # Show first 5
    except Exception as e:
        print(f"Could not get supported algorithms: {e}")

except ImportError as e:
    print(f"Failed to import oqs: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
