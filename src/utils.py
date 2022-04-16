class Utils:
    def get_function_from(class_instance, func_name: str):
        return getattr(class_instance, func_name)
