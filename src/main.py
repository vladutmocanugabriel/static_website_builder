import os, shutil, sys
from src.helpers import clean_public, copy_to_public
from src.blocks import markdown_to_html_node, markdown_to_blocks


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()  
    raise Exception("You're missing the h1 element.")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

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
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    out_dir = os.path.dirname(dest_path)
    os.makedirs(out_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)

        if os.path.isdir(entry_path):
            dst_subdir = os.path.join(dest_dir_path, entry)
            os.makedirs(dst_subdir, exist_ok=True)
            generate_pages_recursive(entry_path, template_path, dst_subdir, basepath)

        elif os.path.isfile(entry_path):
            name, ext = os.path.splitext(entry)
            if ext.lower() != ".md":
                continue

            dest_file = os.path.join(dest_dir_path, name + ".html")
            generate_page(entry_path, template_path, dest_file, basepath)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if not basepath.endswith("/"):
        basepath += "/"

    root = os.getcwd()
    docs_path = os.path.join(root, "docs")
    static_path = os.path.join(root, "static")
    content_path = os.path.join(root, "content")
    template_path = os.path.join(root, "template.html")

    clean_public(docs_path)
    copy_to_public(static_path, docs_path)
    generate_pages_recursive(content_path, template_path, docs_path, basepath)

if __name__ == "__main__":
    main()