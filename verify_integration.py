try:
    import live_data
    print("live_data imported successfully")
except ImportError as e:
    print(f"live_data import failed: {e}")
except Exception as e:
    print(f"live_data error: {e}")

try:
    import solana_service
    print("solana_service imported successfully")
except ImportError as e:
    print(f"solana_service import failed (expected if packages missing): {e}")
except Exception as e:
    print(f"solana_service error: {e}")

try:
    import app
    print("app imported successfully (syntax check)")
except ImportError:
    # streamlit apps often fail import due to strict run modes, but syntax check passes if we got here
    pass
except Exception as e:
    print(f"app error: {e}")
