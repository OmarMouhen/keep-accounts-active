import os

def update_logs(instance):
    try:
        logs_dir = os.path.dirname(instance.formatter.filename)
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        # Append any additional logic here if needed
        instance.logger.info("✅ Logs updated")
    except Exception as e:
        instance.logger.error(f"❌ Failed to update logs: {e}")
