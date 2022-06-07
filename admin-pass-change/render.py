import yaml
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./'))

with open(r'variables.yml') as file:

    render_data = yaml.full_load(file)
    print(render_data)

    template_file = "device_gen.j2"
    render_template = env.get_template(template_file)
    output = render_template.render(render_data)

    with open("device_list.yml", 'a') as f:
        f.write(output)
