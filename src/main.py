import os
from src.helpers import clean_public, copy_to_public
from src.blocks import markdown_to_html_node, markdown_to_blocks


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()  
    raise Exception("You're missing the h1 element.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()

    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    markdown_html_node = markdown_to_html_node(markdown_content)
    markdown_html_string = markdown_html_node.to_html()
    markdown_html_title = extract_title(markdown_content)

    template_content = template_content.replace("{{ Title }}", markdown_html_title)
    template_content = template_content.replace("{{ Content }}", markdown_html_string)

    out_dir = os.path.dirname(dest_path)
    os.makedirs(out_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template_content)

def main():
    root = os.getcwd()
    public_path = os.path.join(root, "public")
    static_path = os.path.join(root, "static")
    content_path = os.path.join(root, "content/index.md")
    template_path = os.path.join(root, "template.html")
    dest_path = os.path.join(public_path, "index.html")

    clean_public(public_path)
    copy_to_public(static_path, public_path)
    generate_page(content_path, template_path, dest_path)

if __name__ == "__main__":
    main()