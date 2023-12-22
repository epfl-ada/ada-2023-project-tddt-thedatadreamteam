import re
import os
import pickle
import warnings

import numpy as np
import pandas as pd
import networkx as nx
import statsmodels.formula.api as smf


def get_similarity(propensity_score1, propensity_score2):
    '''Calculate similarity for instances with given propensity scores'''
    return 1 - np.abs(propensity_score1 - propensity_score2)


warnings.simplefilter(action="ignore", category=FutureWarning)


REMOVE_INTERNATIONAL = True
INTERNATIONAL_LABEL = "International"

if __name__ == "__main__":
    df_articles_all = pd.read_csv(
        os.path.join("Data", "wikispeedia_paths-and-graph", "articles.tsv"),
        delimiter="\t",
        header=None,
        names=["name"],
        skip_blank_lines=True,
        comment="#"
    )

    df_continents = pd.read_csv(os.path.join("Data", "continents.csv"))

    if REMOVE_INTERNATIONAL:
        labeled_articles_all_count = len(df_continents)
        df_continents = df_continents[df_continents.continent != INTERNATIONAL_LABEL]
        labeled_articles_count = len(df_continents)
        print(f"Removing articles labeled as {INTERNATIONAL_LABEL}, Removed articles: {labeled_articles_all_count - labeled_articles_count}")


    df_categories = pd.read_csv(
        os.path.join("Data", "wikispeedia_paths-and-graph", "categories.tsv"),
        delimiter="\t",
        header=None,
        names=["article", "category"],
        skip_blank_lines=True,
        comment="#"
    )

    main_categories = []
    for category in df_categories["category"].values:
        main_categories.append(category.split(".")[1])

    df_categories["categoryMain"] = main_categories


    df_continents_categories = pd.merge(df_continents, df_categories, on="article", how="left")


    df_articles = df_continents_categories[["article", "continent"]].drop_duplicates()
    df_articles = pd.merge(df_articles, df_continents_categories.groupby("article")["categoryMain"].apply(list).reset_index(), on="article")
    df_articles = pd.merge(df_articles, df_continents_categories.groupby("article")["category"].apply(list).reset_index(), on="article")


    plaintext_path = os.path.join("Data", "plaintext_articles")

    word_counts = []
    print("Reading articles")
    for article_name in df_articles.article:
        file_path = os.path.join(plaintext_path, article_name + ".txt")

        with open(file_path, "r", encoding="utf-8") as file:

            _ = file.readline() # Skip the first line because it contains the word #copyright
            content = file.read()

        content = content[:re.search("Retrieved from", content).start(0)]
        word_counts.append(len(content.split()))

    df_articles["length"] = word_counts


    df_pagerank = pd.read_csv(os.path.join("Data", "page_rank.csv"))
    df_articles = pd.merge(df_articles, df_pagerank, on="article", how="left").fillna(0)

    df_paths_finished = pd.read_csv(
        os.path.join("Data", "wikispeedia_paths-and-graph", "paths_finished.tsv"),
        sep="\t",
        header=None,
        names=["hashedIpAddress", "timestamp", "durationInSec", "path", "rating"],
        skip_blank_lines=True,
        comment="#"
    )
    df_paths_unfinished = pd.read_csv(
        os.path.join("Data", "wikispeedia_paths-and-graph", "paths_unfinished.tsv"),
        sep="\t",
        header=None,
        names=["hashedIpAddress", "timestamp", "durationInSec", "path", "target", "motif"],
        skip_blank_lines=True,
        comment="#"
    )

    df_paths_finished["backclicks"] = df_paths_finished["path"].apply(lambda x: x.count("<"))
    df_paths_finished["pathSteps"] = df_paths_finished["path"].apply(lambda x: x.count(";") + 1)
    df_paths_finished["uniqueArticles"] = df_paths_finished["pathSteps"] - df_paths_finished["backclicks"]
    df_paths_finished["path"] = df_paths_finished["path"].apply(lambda x: x.split(";"))
    df_paths_finished["start"] = df_paths_finished["path"].str[0]
    df_paths_finished["target"] = df_paths_finished["path"].str[-1]
    df_paths_finished["isFinished"] = True

    df_paths_unfinished["backclicks"] = df_paths_unfinished["path"].apply(lambda x: x.count("<"))
    df_paths_unfinished["pathSteps"] = df_paths_unfinished["path"].apply(lambda x: x.count(";") + 1)
    df_paths_unfinished["uniqueArticles"] = df_paths_unfinished["pathSteps"] - df_paths_unfinished["backclicks"]
    df_paths_unfinished["path"] = df_paths_unfinished["path"].apply(lambda x: x.split(";"))
    df_paths_unfinished["start"] = df_paths_unfinished["path"].str[0]
    df_paths_unfinished["isFinished"] = False

    df_paths = pd.concat([df_paths_finished, df_paths_unfinished])
    df_paths = df_paths[df_paths["start"].isin(df_articles_all.name) & df_paths["target"].isin(df_articles_all.name)]


    print("Computing Shortest Paths")
    shortest_paths = []
    with open(os.path.join("Data", "wikispeedia_paths-and-graph", "shortest-path-distance-matrix.txt")) as file:
        for line in file:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            shortest_paths.append(list(map(lambda x: -1 if x == "_" else int(x), list(line))))
            
    shortest_paths = np.array(shortest_paths)

    df_shortest_paths = pd.DataFrame(shortest_paths, index=df_articles_all.name, columns=df_articles_all.name)
    df_paths["shortestPath"] = df_paths.apply(lambda row: df_shortest_paths.loc[row["start"], row["target"]], axis="columns")
    df_paths = df_paths[df_paths["shortestPath"] >= 0]


    df_articles_target = df_articles.copy()
    df_articles_target.columns = [column[0].upper() + column[1:] for column in df_articles_target.columns]
    df_articles_target = df_articles_target.add_prefix("target")

    df_paths_articles = pd.merge(df_paths, df_articles_target, left_on="target", right_on="targetArticle", suffixes=["", ]).drop(columns="targetArticle")

    df_start_articles = df_articles.copy()
    df_start_articles.columns = [column[0].upper() + column[1:] for column in df_start_articles.columns]
    df_start_articles = df_start_articles.add_prefix("start")
    df_paths_articles = pd.merge(df_paths_articles, df_start_articles, left_on="start", right_on="startArticle", suffixes=["", ]).drop(columns="startArticle")

    df_paths_articles["isFinishedInt"] = df_paths_articles["isFinished"].astype(int)


    df_analysis = df_paths_articles.copy()
    df_analysis = df_analysis.fillna(0)
    df_analysis["treatment"] = df_analysis.targetContinent == "Europe"

    print("df_analysis:", df_analysis.shape)

    eq = "isFinishedInt ~ startLength + startPageRank + targetLength + targetPageRank"

    model = smf.logit(eq, df_analysis).fit()

    df_analysis["propensityScore"] = model.predict()

    print(model.summary())

    treatment_df = df_analysis[df_analysis["treatment"]]
    control_df = df_analysis[~df_analysis["treatment"]]
    def get_similarity(propensity_score1, propensity_score2):
        '''Calculate similarity for instances with given propensity scores'''
        return 1 - np.abs(propensity_score1 - propensity_score2)

    print("Computing Matching..")
    G = nx.Graph()
    
    for control_id, control_row in control_df.iterrows():
        print(f'{control_id} of {len(control_df)}')
        for treatment_id, treatment_row in treatment_df.iterrows():

            if len(set(treatment_row['startCategoryMain']) & set(control_row['startCategoryMain'])) \
            and len(set(treatment_row['targetCategoryMain']) & set(control_row['targetCategoryMain'])) \
            and treatment_row["shortestPath"] == control_row["shortestPath"]:
                weight = get_similarity(treatment_row["propensityScore"], control_row["propensityScore"])
                G.add_edge(treatment_id, control_id, weight=weight)

    matching = nx.max_weight_matching(G)

    print("matching:", len(matching))

    with open("matching.pkl", "wb") as file:
        pickle.dump(matching, file)
