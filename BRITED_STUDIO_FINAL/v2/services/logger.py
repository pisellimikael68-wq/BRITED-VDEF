class PipelineLogger:

    @staticmethod
    def section(title: str):
        print("\n========================")
        print(title.upper())
        print("========================")

    @staticmethod
    def info(message: str):
        print(message)

    @staticmethod
    def success(message: str):
        print(f"✅ {message}")

    @staticmethod
    def warning(message: str):
        print(f"⚠️ {message}")

    @staticmethod
    def separator():
        print()