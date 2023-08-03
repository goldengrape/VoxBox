from AI_process import structured_input
import pandas as pd
from data_process import (
    get_containers_as_text,
    add_data,
    print_tree,)

def add_item_from_human_input(df, human_input,debug=False):
    known_containers = get_containers_as_text(df)
    current_id=int(df['id'].max())+1
    result=structured_input(
        human_input=human_input, 
        current_id=current_id, known_containers=known_containers, debug=debug)
    new_df=add_data(df, result)
    return new_df 