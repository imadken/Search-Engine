def parse_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content

def Load_queries(path="lisa/LISA.QUE"):
    id_content_dict = {}
    file_content = parse_file(path)
    lines = file_content.split('\n')
    current_id = None
    current_content = []

    for line in lines:
        if line.isdigit():
            # If a new ID is found, update current_id and store the previous content
            if current_id is not None:
                id_content_dict[current_id] = ' '.join(current_content).replace("#",'').strip()
            current_id = line
            current_content = []
        else:
            current_content.append(line)

    # Add the last entry to the dictionary
    if current_id is not None:
        id_content_dict[current_id] = ' '.join(current_content).strip()

    return id_content_dict

def Load_relevance(path="lisa/LISA.REL"):
    file_content = parse_file(path)
    lines = file_content.split('\n')
    current_query_id = None
    query_rel = dict()

    for line in lines:
        if line.startswith('Query'):
            # If a new query is found, update current_query_id and store the previous references
            current_query_id = line.split()[1]
        elif line.endswith(':')== False and line!= "" :
        # elif line.startswith('2 Relevant Refs:') or line.startswith('5 Relevant Refs:') or line.startswith('7 Relevant Refs:'):
            # Extract relevant references and add them to the current_references list
            references = [int(ref) for ref in line.split() if ref != '-1']
            query_rel[current_query_id] = references
        
    return query_rel

if __name__ =="__main__":
    
    # print(Load_queries(parse_file("lisa/LISA.QUE"))["1"])
    # print(Load_relevance(parse_file("lisa/LISA.REL"))["1"])
    print(Load_relevance())
    # print(Load_queries())

    