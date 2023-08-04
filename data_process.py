import pandas as pd
import gzip

def add_data(df: pd.DataFrame, data_list: list) -> pd.DataFrame:
    """
    Add data to the DataFrame.

    Args:
        df: The DataFrame to add data to.
        data_list: The list of data to add.

    Returns:
        The updated DataFrame.
    """

    return pd.concat([df, pd.DataFrame(data_list)], ignore_index=True)


def get_containers_as_text(df: pd.DataFrame) -> str:
    """
    Get the text representation of the containers.

    Args:
        df: The DataFrame of containers.

    Returns:
        The text representation of the containers.
    """

    all_ids = set(df['id'])
    all_parent_ids = set(df['parent_id'].dropna())
    container_ids = all_ids.intersection(all_parent_ids)
    container_df = df[df['id'].isin(container_ids)]
    # container_text = container_df[['id', 'name']].to_csv(index=False)
    container_text = container_df.to_csv(index=False)
    return container_text

def get_item_path(df: pd.DataFrame, name: str) -> str:
    """
    Get the path of the item.

    Args:
        df: The DataFrame of items.
        name: The name of the item.

    Returns:
        The path of the item.
    """

    if name not in df['name'].values:
        return f'物品 {name} 未找到'
    else:
        item = df[df['name'] == name].iloc[0]
        path = [name]
        while item['parent_id'] != '':
            parent_items = df[df['id'] == item['parent_id']]
            if parent_items.empty:
                break
            item = parent_items.iloc[0]
            path.insert(0, item['name'])
        return '>'.join(path)

def closest_word(query: str, words: list, topK: int = 3) -> list:
    """
    Get the closest words to the query.

    Args:
        query: The query word.
        words: The list of words.
        topK: The number of closest words to return.

    Returns:
        The list of closest words.
    """

    words.sort(key=lambda x: gzip_distance(query, x))
    return words[:topK]

def gzip_distance(x1: str, x2: str) -> float:
    """
    Calculate the gzip distance between two strings.

    Args:
        x1: The first string.
        x2: The second string.

    Returns:
        The gzip distance between the two strings.
    """

    Cx1 = len(gzip.compress(x1.encode()))
    Cx2 = len(gzip.compress(x2. encode()))
    x1x2 = " ".join([x1, x2])
    Cx1x2 = len(gzip.compress(x1x2. encode()))
    ncd = (Cx1x2 - min(Cx1, Cx2)) / max(Cx1, Cx2)
    return ncd

def path_query(query: str, df: pd.DataFrame,topK: int = 3) -> list:
    """
    Get the paths of the items matching the query.

    Args:
        query: The query.
        df: The DataFrame of items.

    Returns:
        The list of paths of the items matching the query.
    """

    candidate_list = closest_word(query, df.name.to_list(),topK=topK)
    path_list = [get_item_path(df, c) for c in candidate_list]
    return path_list

def move_container(df, container_name, new_parent_name):
    container_id = df[df['name'] == container_name]['id'].values[0]
    new_parent_id = df[df['name'] == new_parent_name]['id'].values[0]
    df.loc[df['id'] == container_id, 'parent_id'] = new_parent_id
    return df

def print_tree(df, node_id=None, prefix="", is_last=False):
    if node_id is None:
        node = df[df['parent_id'].isnull()].iloc[0]
    else:
        node = df[df['id'] == node_id].iloc[0]

    # if node['name'] != 'Root':
    prefix_component = "└─ " if is_last else "├─ "
    print(prefix + prefix_component + node['name'])

    children = df[df['parent_id'] == node['id']]
    prefix_for_children = prefix + ("   " if is_last else "│  ")
    for i, (_, child) in enumerate(children.iterrows()):
        print_tree(df, child['id'], prefix_for_children, i == len(children) - 1)