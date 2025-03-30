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
            color: #00aa00; /* Green */
        }
        .con-args {
            font-size: 12px;
            color: #ff0000; /* Red */
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