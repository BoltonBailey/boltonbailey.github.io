
import os


def md_to_html(in_file, out_file):
    """
    Convert a .md file with filename in_file to a .html file with filename
    out_file using pandoc.
    """
    print(f"Converting {in_file} to {out_file}")
    os.system(f"pandoc {in_file} -f markdown -t html -s -o tmp.txt")
    # Replace links to .md to links to .html
    tmp = open("tmp.txt", "r")
    out = open(out_file, "w")

    for line in tmp:
        out.write(line.replace(".md", ".html"))

    os.system("rm tmp.txt")


# Copy all files from /source to /target, pandocing .md files to .html
for dirpath, _, filenames in os.walk("source"):

    if "." in dirpath:
        continue

    print(f"Scanning {dirpath}")
    new_dirpath = dirpath.replace("source", "target")

    if not os.path.exists(f"{new_dirpath}"):
        os.mkdir(f"{new_dirpath}")
    for filename in filenames:
        if filename.endswith(".md"):
            new_filename = filename.replace(".md", ".html")
            md_to_html(f"{dirpath}/{filename}",
                       f"{new_dirpath}/{new_filename}")
        else:
            print(f"Copying {dirpath}/{filename} to {new_dirpath}/{filename}")
            os.system(f"cp {dirpath}/{filename} {new_dirpath}/{filename}")

# For the about.md file, copy in
