import re

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
        # Robust check for section start (ignore extra spaces, emoji, etc.)
        if re.match(rf"^\s*##+\s*✅?\s*{re.escape(section)}\s*$", line):
            inside_section = True
            continue
        if inside_section:
            # Next section: any line starting with ## or ###
            if re.match(r"^\s*##+", line):
                break
            if "- [x]" in line.lower():
                done += 1
                total += 1
            elif "- [ ]" in line.lower():
                total += 1
    return int((done / total) * 100) if total else 0

def update_badge(line, percent):
    # Replace the percentage in the badge URL (e.g., -14%25-)
    return re.sub(r'-(\d+)%25-', f'-{percent}%25-', line)

with open("README.md", "r", encoding="utf-8") as file:
    lines = file.readlines()

new_lines = []
for line in lines:
    updated = False
    for title, label in sections.items():
        if label in line:
            progress = get_progress(lines, title)
            print(f"{title} progress: {progress}%")  # Debug output
            new_line = update_badge(line, progress)
            new_lines.append(new_line)
            updated = True
            break
    if not updated:
        new_lines.append(line)

with open("README.md", "w", encoding="utf-8") as file:
    file.writelines(new_lines)
