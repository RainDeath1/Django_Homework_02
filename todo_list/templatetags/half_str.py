from django import template

register = template.Library()


@register.filter
def half_str(value):
    return value[:len(value) // 2]


@register.tag(name='split_string')
def split_string(parser, token):
    try:
        tag_name, value, separator, _, variable_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Тег %r требует два аргумента (строку и разделитель) и переменную для "
                                           "хранения результата"
                                           % token.contents.split()[0])
    return SplitStringNode(value, separator, variable_name)


class SplitStringNode(template.Node):
    def __init__(self, value, separator, variable_name):
        self.value = template.Variable(value)
        self.separator = template.Variable(separator)
        self.variable_name = variable_name

    def render(self, context):
        value = self.value.resolve(context)
        separator = self.separator.resolve(context)
        context[self.variable_name] = value.split(separator)
        return ''


@register.filter
def reverse_string(value):
    return value[::-1]


@register.filter
def multiplier(value, arg=1):
    try:
        value = float(value)
        arg = float(arg)
        return arg * value
    except ValueError:
        return value


@register.tag
def repeat_string(parser, token):
    try:
        tag_name, value, times = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Тег %r требует два аргумента: строку и количество повторений."
                                           % token.contents.split()[0])
    return RepeatStringNode(value, times)


class RepeatStringNode(template.Node):
    def __init__(self, value, times):
        self.value = template.Variable(value)
        self.times = int(times)

    def render(self, context):
        value = self.value.resolve(context)
        return value * self.times


@register.tag
def greeting(parser, token):
    try:
        tag_name, hour = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Теуг %r требует один аргумент: час"
                                           % token.split_contents()[0])
    return GreetingNode(hour)


class GreetingNode(template.Node):
    def __init__(self, hour):
        self.hour = int(hour)

    def render(self, context):
        if 0 <= self.hour < 12:
            return "Доброе утро"
        elif 12 <= self.hour < 18:
            return "Добрый день"
        else:
            return "Добрый вечер"


