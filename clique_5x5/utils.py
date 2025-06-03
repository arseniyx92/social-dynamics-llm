def debug_print(text):
    with open("log1.txt", "a") as file:
        file.write(text)

def create_html(filename):
    with open(filename, "w") as visual:
        visual.write("""
<!DOCTYPE html>
<html>
<head>
    <style>
        .agent-container {
            font-family: Arial, sans-serif;
            margin: 10px;
            padding: 10px;
            font-size: 20px;
        }
        .pro-args {
            font-size: 12px;
            color: #e600ff;
        }
        .con-args {
            font-size: 12px;
            color: #3c00ff;
        }
        .agent-id {
            font-weight: bold;
        }
        .agent-text-0 {
            font-style: italic;
            color: #ff0000; /* Red */
        }
        .agent-text-1 {
            font-style: italic;
            color: #ff6600; /* Orange-red */
        }
        .agent-text-2 {
            font-style: italic;
            color: #ffcc00; /* Yellow-orange */
        }
        .agent-text-3 {
            font-style: italic;
            color: #66cc00; /* Yellow-green */
        }
        .agent-text-4 {
            font-style: italic;
            color: #00aa00; /* Green */
        }
    </style>
</head>
<body>
<div class="agent-container">
Color map:\n
<span class="agent-text-0">strictly against</span>\n
<span class="agent-text-1">against but not sure</span>\n
<span class="agent-text-2">neutral</span>\n
<span class="agent-text-3">in favor but not sure</span>\n
<span class="agent-text-4">strictly in favor</span>\n
</div>
        """)

def finish_with_html(filename):
    with open(filename, "a") as visual:
        visual.write("""
</body>
</html>
        """)

def message_to_html(filename, text):
    with open(filename, "a") as visual:
        visual.write(text)