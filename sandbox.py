from dynamic_executor import DynamicModeExecutor

if __name__ == "__main__":
    for error_message in DynamicModeExecutor().execute(locals(), globals()):
        pass
