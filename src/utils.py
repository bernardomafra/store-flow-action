class Utils:
    def get_function_from(class_instance, func_name: str):
        print(f"NAME: {func_name}")
        return getattr(class_instance, func_name)
