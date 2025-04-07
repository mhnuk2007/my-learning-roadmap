import re

# Define sections and corresponding badge lines
sections = {
    "Git & GitHub": "Git%20%26%20GitHub",
    "Java": "Java",
    "Spring Boot": "Spring%20Boot",
    "Docker": "Docker",
    "AWS": "AWS",
    "Google Cloud": "GCP",
    "DevOps": "DevOps"
}

def get_progress(lines, section):
    inside_section = False
    total = done = 0
    for line in lines:
        if section in line:
            inside_section = True
            continue
        if inside_section:
            if line.startswith("## "):  # next section starts
                break
            if "- [x]" in line.lower():
                done += 1
                total += 1
            elif "- [ ]" in line.lower():
                total += 1
    return int((done / total) * 100) if total else 0

def update_badge(line, percent):
    return re.sub(r'\d+%25', f"{percent}%25", line)

with open("README.md", "r", encoding="utf-8") as file:
    lines = file.readlines()

new_lines = []
for line in lines:
    updated = False
    for title, label in sections.items():
        if label in line:
            progress = get_progress(lines, f"## ✅ {title}")
            new_line = update_badge(line, progress)
            new_lines.append(new_line)
            updated = True
            break
    if not updated:
        new_lines.append(line)

with open("README.md", "w", encoding="utf-8") as file:
    file.writelines(new_lines)
