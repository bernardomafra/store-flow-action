from string import Template
from src.constants import Constants

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

    def txt_file_to_dict(filename: str, delimiter: str, header_to_discard: str, key_map: dict):
        try:
            resolver: dict = {}
            with open(Constants.FILE_BASE_PATH + filename, 'r') as file:
                content = file.read()
                for line in content.splitlines():
                    if header_to_discard in line:
                        continue
                    line_content = line.split(delimiter)
                    department_name = line_content[0] if line_content[0] != "" else Constants.NO_DEPARTMENT 
                    resolver[department_name] = resolver[department_name] if department_name in resolver else []
                    product = f"{line_content[2] if line_content[2].isnumeric() else '0'}{Constants.PRODUCT_LINE_DIVIDER}{line_content[1]}"
                    resolver[department_name].append(product)
                return output
        except Exception as error:
            print(error)
            return []