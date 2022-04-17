from string import Template


class Utils:
    def get_function_from(class_instance, func_name: str):
        return getattr(class_instance, func_name)

    def replace_product_name(sentence: str, product: str):
        if "product" in sentence:
            template_obj = Template(sentence)
            sentence = template_obj.substitute(product=product)
        return sentence
        

