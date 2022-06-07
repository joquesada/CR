import yaml
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./'))

with open(r'variables_scdc2.yml') as file:

    render_data = yaml.full_load(file)
    print(render_data)

    template_file = "device_gen_scdc2.j2"
    render_template = env.get_template(template_file)
    output = render_template.render(render_data)

    with open("device_list_scdc2.yml", 'a') as f:
        f.write(output)
