import numpy as np
import networkx as nx
import pandas as pd

def page_rank(adjacency_matrix, dumping_factor=0.85, max_iterations=1000):
  # Initialize the PageRank scores with a uniform distribution
  num_nodes = adjacency_matrix.shape[0]
  page_rank_scores = np.ones(num_nodes) / num_nodes
  num_links = np.sum(adjacency_matrix,axis=1)

  # Iteratively update the PageRank scores
  for _ in range(max_iterations):
    # Perform the matrix-vector multiplication
    shared_page_rank = page_rank_scores/num_links
    shared_page_rank[np.isinf(shared_page_rank)] = 0
    
    new_page_rank_scores = adjacency_matrix.T.dot(shared_page_rank)

    # Add the teleportation probability
    new_page_rank_scores = (1-dumping_factor)/num_nodes + dumping_factor * new_page_rank_scores
    # Check for convergence
    if np.allclose(page_rank_scores, new_page_rank_scores):
        break

    page_rank_scores = new_page_rank_scores
    return page_rank_scores

def csv_pagerank():
    df = pd.read_table('data/wikispeedia_paths-and-graph/links.tsv', header=None, names = ['Articles','Links'], skiprows=12)

    #We create the graph of all the wikispeedia game
    G = nx.from_pandas_edgelist(df, 'Articles', 'Links', create_using=nx.DiGraph())

    node_labels = list(G.nodes())
    node_indices = {node: index for index, node in enumerate(node_labels)}

    #Adjacency Matrix
    adjacency_matrix = nx.adjacency_matrix(G).todense()

    page_ranks = page_rank(adjacency_matrix)
    
    dataset = {'Articles': node_labels, 'PageRank':page_ranks}

    articles_rank = pd.DataFrame(dataset)
    articles_rank=articles_rank.sort_values(by='PageRank',ascending=False)
    
    articles_rank.to_csv('data/pagerank.csv',index=False)