import os
import re

html_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove dead functions: renderExample, setExampleTab, toggleDialogueMode, speakCurrentExample
# Remove setExampleTab
html = re.sub(r'function setExampleTab\([\s\S]*?\}\n', '', html)

# Remove toggleDialogueMode
html = re.sub(r'function toggleDialogueMode\([\s\S]*?\}\n', '', html)

# Remove renderExample
html = re.sub(r'function renderExample\([\s\S]*?\}\n', '', html)

# Remove speakCurrentExample
html = re.sub(r'function speakCurrentExample\([\s\S]*?\}\n', '', html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Dead code removed successfully!")
