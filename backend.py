from AI_process import (
    structured_input,
    query_item,
    better_query,
    structured_container_mover,
    structured_takeout_items,
    interpret_human_command,
    )
from data_process import (
    get_containers_as_text,
    add_data,
    path_query,
    move_container,
    takeout_item_list,
    )
import pandas as pd

def generate_tree_string(df, node_id=None, prefix="", is_last=False):
    result = ""
    if node_id is None:
        node = df[df['parent_id'].isnull()].iloc[0]
    else:
        node = df[df['id'] == node_id].iloc[0]

    prefix_component = "└─ " if is_last else "├─ "
    result += prefix + prefix_component + node['name'] + "\n"

    children = df[df['parent_id'] == node['id']]
    prefix_for_children = prefix + ("   " if is_last else "│  ")
    for i, (_, child) in enumerate(children.iterrows()):
        result += generate_tree_string(df, child['id'], prefix_for_children, i == len(children) - 1)
    return result


def add_item_from_human_input(df, human_input,debug=False):
    known_containers = get_containers_as_text(df)
    current_id=int(df['id'].max())+1
    result=structured_input(
        human_input=human_input, 
        current_id=current_id, known_containers=known_containers, debug=debug)
    if debug:
        print(result)
    new_df=add_data(df, result)
    return new_df 

def query_item_from_human_query(df, human_query,debug=False):
    better_human_query=better_query(human_query)
    if debug:
        print(better_human_query)
    ref_path=",".join(path_query(better_human_query, df))
    if debug:
        print(ref_path)
    answer=query_item(human_query, ref_path=ref_path)    
    return answer

def move_container_by_human_command(df, human_cmd,debug=False):
    moving_names=structured_container_mover(human_cmd)
    if debug:
        print(moving_names)
    if moving_names['new_parent_name'] not in df['name'].values:
        if debug:
            print('new parent not in database')
        df=add_item_from_human_input(df, moving_names['new_parent_name'])
    df=move_container(df, 
        moving_names["container_name"], 
        moving_names['new_parent_name'])
    if debug:
        print(generate_tree_string(df))
    return df

def takeout_items_by_human_command(df, human_cmd,debug=False):
    takeout_items=structured_takeout_items(human_cmd)
    if debug:
        print(takeout_items)
    df=takeout_item_list(df,takeout_items)
    if debug:
        print(generate_tree_string(df))
    return df

def run_human_command(df, human_cmd, debug=False):
    command_list=interpret_human_command(human_cmd)
    print(command_list)
    answer_list=[]

    for command in command_list:
        name=command['name']
        human_input=command['Human_command']
        if debug:
            print(name, human_input)
        if name=='query_item_from_human_query':
            answer=query_item_from_human_query(df,human_input)
            answer_list.append(answer)
            if debug:
                print(answer)
        else:
            df=eval(name)(df, human_input)
            if debug:
                print(generate_tree_string(df))
    return df, answer_list