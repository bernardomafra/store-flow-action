from string import Template

class Utils:
    def get_function_from(class_instance, func_name: str):
        return getattr(class_instance, func_name)

    def replace_variable_in_sentence(sentence: str, variable_key: str, variable_value: str):
        try:
            print(f"Replace {variable_key} with {variable_value} in {sentence}")
            if variable_key in sentence:
                template_obj = Template(sentence)
                to_replace = {}
                to_replace[variable_key] = variable_value
                sentence = template_obj.substitute(**to_replace)
                print(variable_key, variable_value, sentence)
            return sentence
        except Exception as error:
            print(error)
            return ""
        

