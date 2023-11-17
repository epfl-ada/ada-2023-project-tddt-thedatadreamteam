# GeoWiki

## Abstract

As online educational platforms increasingly become vital tools for knowledge dissemination, examining potential biases that may influence user experiences and content representation is crucial. For this reason, in this project, we aim to investigate the presence of geographical biases in the Wikispeedia game and in the behaviour of its players. Wikispeedia is a game where the goal is to get from one article to another using links. The more someone is aware of potential links between articles, the more likely he/she is to succeed.

Based on the origin of the dataset, the [2007 Wikipedia Selection for schools](https://web.archive.org/web/20071006054112/http://schools-wikipedia.org/), which is targeted for children in the UK, and the origin of Wikispeedia itself (Canada), we want to observe if there is a bias towards the regions of North America and Europe (collectively) in the selection of the articles and in the way people play the game.

## Research questions

To correctly answer if there is a bias towards Europe and North America (NA), we will propose and answer the following research questions:

- Is there a difference in article distribution between Europe/NA and the other continents?
- Are there differences in paths' statistics for articles with the target articles related to Europe/NA and with the target articles associated with the other continents?

We aim to conduct an observational study, controlling all the confounding factors that could bias our analysis, in which the games with a target article related to Europe/NA belong to the treatment group, and the games with a target article associated with the other continents are the control group.

### Supporting questions:

- Is there a difference in path length, success rate, restart rate, and time spent for paths with a target article related to a different continent from Europe and NA?
- Do people back-click more from articles unrelated to NA or Europe?

## Methods

### Article category

We start with the geographical categories that are predefined in our Wikispeedia dataset. This allows us to label countries, cities and geographical articles from specific geographic locations:
- African_Geography
- Antarctica
- Central_and_South_American_Geography
- European_Geography
- Geography_of_Asia
- Geography_of_Oceania_Australasia
- Geography_of_the_Middle_East
- North_American_Geography

The geographic locations are renamed and grouped into standard continent names. We can extend our list by searching for keywords (from already labeled articles) in the article names. This allows us to label articles from categories such as British_History, Monarcs_of_United_Kingdom, America_History or USA_presidents with examples of article names Napoleon_I_of_**France** and 1755_**Lisbon**_earthquake.

Then, for labeling the rest of the articles, we propose the following methods:

- Our first idea was to use the semantic distance between articles and look for the geographical one closest to our article. However, this method may include bias towards article paths, as the article [Wikispeedia: An Online Game for Inferring Semantic Distances between Concepts](http://infolab.stanford.edu/~west1/pubs/West-Pineau-Precup_IJCAI-09.pdf) uses players' paths to estimate the semantic distance.
- Using weighted links: We calculated the position of the links in the articles and sorted them accordingly, assigning more weight to the first links. We calculated weighted scores of the continent categories for the new articles using the already labelled links. When selecting the label with the highest score, we observed promising results for the People category.
- Analyzing the first paragraph: By looking at the information at the beginning of the articles, we can extract the locations, origins and other information related to the already labeled articles.
- Looking at the whole article: This idea transforms the articles into vectors and applies a clustering method to them, with the origins of the clusters in the continental articles.
- Category non-continental: There are plenty of articles that are general and could not be assigned to a continent. We can simplify our analysis by setting some categories like Business or Animal Rights to non-continental and some articles that have no links related to nothing geographical as non-continental.

### Observational study

After the article labeling step, we will conduct an observational study using the treated and control groups model seen in the class. We will analyze the available attributes (length, success rate, time spent, number of back clicks, etc.) of paths in the treated and control groups. We expect to find a trend indicating that paths with target topics associated with Europe/NA have a higher success rate due to a knowledge foundation.

As in every observational study, an important step is matching. The following factors can be used to match games:

- Starting article
- The [PageRank](https://es.wikipedia.org/wiki/PageRank) of the goal (indicates the same probability of reaching the goal). Already computed in the file ```Data/pagerank.csv```
- Same category of the target article


## Proposed milestones for P3 and Timeline

| Date | Milestone |
|------------|-----|
| 17.11.2023 | Deliver P2 |
| 24.11.2023 | Finalize articles selection |
| 04.12.2023 | General analysis of the data and observational study start |
| 10.12.2023 | Observational study finished |
| 14.12.2023 | Finalizing Visualizations |
| 20.12.2023 | Data Story finished |
| 22.12.2023 | Deadline |

## Organization within the team

As this project is a huge opportunity to learn and grow, we organized ourselves in Agile methodology. We work in weekly sprints and meet regularly multiple times a week. Each member works on each part of the pipeline to learn the most from this course. We then meet and discuss our solutions and combine the best ideas for the final analysis. We then plan goals for the next sprint so that the project can progress smoothly and we will be able to deliver an engaging data story about geographical influence in the wikispeedia game.

## __Questions for the TA__

- Should we construct a control/treatment group differently?
- Or conduct multiple observational analyses?
   - For example, searching for biases for individual continents with one continent as the treatment group and the others as the control group.
