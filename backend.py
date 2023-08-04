from AI_process import (
    structured_input,
    query_item,
    better_query,
    structured_container_mover,)
from data_process import (
    get_containers_as_text,
    add_data,
    path_query,
    move_container,
    print_tree,)
import pandas as pd

def add_item_from_human_input(df, human_input,debug=False):
    known_containers = get_containers_as_text(df)
    current_id=int(df['id'].max())+1
    result=structured_input(
        human_input=human_input, 
        current_id=current_id, known_containers=known_containers, debug=debug)
    new_df=add_data(df, result)
    return new_df 

def query_item_from_human_query(df, human_query):
    better_human_query=better_query(human_query)
    ref_path=",".join(path_query(better_human_query, df))
    answer=query_item(human_query, ref_path=ref_path)
    return answer

def move_container_by_human_command(df, human_cmd):
    moving_names=structured_container_mover(human_cmd)
    df=move_container(df, 
        moving_names["container_name"], 
        moving_names['new_parent_name'])
    return df