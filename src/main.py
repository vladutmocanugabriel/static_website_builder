import os, shutil
from src.helpers import clean_public, copy_to_public
from src.blocks import markdown_to_html_node, markdown_to_blocks


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()  
    raise Exception("You're missing the h1 element.")

def generate_page(from_path, template_path, dest_path):
    #print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(from_path, "r") as markdown_file:
        print(f"We're opening and reading the file from: {from_path}")
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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)

        if os.path.isdir(entry_path):
            dst_subdir = os.path.join(dest_dir_path, entry)
            os.makedirs(dst_subdir, exist_ok=True)
            generate_pages_recursive(entry_path, template_path, dst_subdir)

        elif os.path.isfile(entry_path):
            name, ext = os.path.splitext(entry)
            if ext.lower() != ".md":
                continue

            dest_file = os.path.join(dest_dir_path, name + ".html")
            generate_page(entry_path, template_path, dest_file)
            
            


    pass

def main():
    root = os.getcwd()
    public_path = os.path.join(root, "public")
    static_path = os.path.join(root, "static")
    content_path = os.path.join(root, "content")
    template_path = os.path.join(root, "template.html")
    dest_path = os.path.join(public_path, "index.html")

    clean_public(public_path)
    copy_to_public(static_path, public_path)
    generate_pages_recursive(content_path, template_path, public_path)

if __name__ == "__main__":
    main()