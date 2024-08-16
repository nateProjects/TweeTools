import json
import re
import os
import sys
import uuid

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def canvas_to_twee(canvas_json):
    data = json.loads(canvas_json)
    twee_output = ":: StoryTitle\nCanvas\n\n:: StoryData\n{\n  \"ifid\": \"YOUR-IFID-HERE\",\n  \"format\": \"Harlowe\",\n  \"format-version\": \"3.3.9\",\n  \"start\": \"Start Passage\",\n  \"zoom\": 1\n}\n\n"

    connections = {}
    for edge in data['edges']:
        from_node = edge['fromNode']
        to_node = edge['toNode']
        if from_node not in connections:
            connections[from_node] = []
        connections[from_node].append(to_node)

    for node in data['nodes']:
        node_id = node['id']
        node_text = node.get('text', '')
        x, y = node['x'], node['y']
        width, height = node['width'], node['height']

        twee_output += f":: {node_text} {{\"position\":\"{x+825},{y+725}\",\"size\":\"{width},{height}\"}}\n"
        
        if node_id in connections:
            for to_node in connections[node_id]:
                to_node_text = next((n['text'] for n in data['nodes'] if n['id'] == to_node), None)
                if to_node_text:
                    twee_output += f"[[{to_node_text}]]\n"
                else:
                    print(f"Warning: Could not find text for node {to_node}")
        
        twee_output += "\n\n"

    return twee_output

def twee_to_canvas(twee_content):
    passages = re.split(r'\n*:: ', twee_content)[1:]  # Split by ':: ' and remove the first empty element
    nodes = []
    edges = []
    node_id_map = {}  # Map to store node titles and their corresponding random IDs
    
    for passage in passages:
        if passage.startswith('StoryTitle') or passage.startswith('StoryData'):
            continue
        
        lines = passage.split('\n')
        title_and_metadata = lines[0].split('{')
        title = title_and_metadata[0].strip()
        
        if len(title_and_metadata) > 1:
            try:
                metadata = json.loads('{' + title_and_metadata[1])
                position = metadata['position'].split(',')
                size = metadata['size'].split(',')
                x, y = int(position[0]) - 825, int(position[1]) - 725  # Adjust for the offset
                width, height = map(int, size)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Warning: Error parsing metadata for passage '{title}'. Using default values. Error: {e}")
                x, y, width, height = 0, 0, 250, 60  # Default values
        else:
            x, y, width, height = 0, 0, 250, 60  # Default values
        
        node_id = str(uuid.uuid4())[:14]  # Generate a random ID (first 14 characters of a UUID)
        node_id_map[title] = node_id
        nodes.append({
            "id": node_id,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "type": "text",
            "text": title
        })
        
        # Find links in the passage content
        for line in lines[1:]:
            links = re.findall(r'\[\[(.*?)\]\]', line)
            for link in links:
                if link in node_id_map:
                    edges.append({
                        "id": f"edge_{uuid.uuid4().hex[:14]}",
                        "fromNode": node_id,
                        "toNode": node_id_map[link],
                        "fromSide": "bottom",
                        "toSide": "top"
                    })
                else:
                    print(f"Warning: Link '{link}' in passage '{title}' does not correspond to any existing passage.")
    
    return json.dumps({"nodes": nodes, "edges": edges}, indent=2)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    file_name, file_extension = os.path.splitext(input_file)

    try:
        if file_extension.lower() == '.canvas':
            # Convert Canvas to Twee
            canvas_content = read_file(input_file)
            twee_output = canvas_to_twee(canvas_content)
            output_file = f"{file_name}.twee"
            write_file(output_file, twee_output)
            print(f"Converted Canvas to Twee. Output saved to {output_file}")
        elif file_extension.lower() == '.twee':
            # Convert Twee to Canvas
            twee_content = read_file(input_file)
            canvas_output = twee_to_canvas(twee_content)
            output_file = f"{file_name}.canvas"
            write_file(output_file, canvas_output)
            print(f"Converted Twee to Canvas. Output saved to {output_file}")
        else:
            print("Unsupported file format. Please use .canvas or .twee files.")
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
