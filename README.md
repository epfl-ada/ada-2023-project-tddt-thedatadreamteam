# Europe in Wikispeedia - Unmasking Geographical Bias 
*TheDataDreamTeam (TDDT): Jason Becker, Ruben Jungius, Juan Enrique Martín, Pablo Menéndez, Jiri Pospisil*

## Datastory
[Europe in Wikispeedia - Unmasking Geographical Bias ](https://rjungius.github.io)

## Abstract

As online educational platforms increasingly become vital tools for knowledge dissemination, it is crucial to examine potential biases that may influence user experiences and content representation. For this reason, in this project we aim to investigate the presence of geographical biases in the Wikispeedia game and in the behavior of its players. Wikispeedia is a game where the goal is to get from one article to another by using links, the more someone is aware of potential links between articles, the more likely he/she is to succeed.

Based on the origin of the dataset, the [2007 Wikipedia Selection for schools](https://web.archive.org/web/20071006054112/http://schools-wikipedia.org/), which is targeted for children in the UK, and the origin of Wikispeedia itself (Canada), we want to observe if there is a bias towards the region of Europe in the selection of articles and in the way people play the game.

## Research questions

To correctly answer if there is a bias towards Europe we will propose and answer the following research questions:

- Are there more articles for Europe than for the other continents?
- Are there more articles from Europe in the paths than there should be?

We conducted an observational study where the treatment group were the games whose paths that end in Europe classified articles and the control group the games that end in other continents related articles. Our objective is to minimize the confounding factors that could bias our analysis so we can analyze paths where the difference is only the goal.

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

Then, for classifying the rest of the articles we made use of ChatGPT. Our method was sending all the titles of the articles in batches of around 300 and ask the LLM to classify them based on. After that, we compared to the prior classification and classified manually those that were not the same (usually ChatGPT was right).

### Observational study

After we classified the articles, we conduct an observational study using a model like in the case of the treated and control case seen in class. We compare the performance of the players in the treatment and control groups. We define performance as the success rate, that is, the number of finished paths in each group. We expected to find a trend indicating that paths leading to topics that can be associated with Europe have a higher play and completion rate due to a knowledge foundation. 

As in every observational study, an important step is matching. We performed matching on:

- Category of the starting article
- Category of the target article
- Shortest path

To make sure we balance the dataset, we compute the propensity score on observed covariates via logistic regression:

- Length of the starting article
- Length of the target article
- PageRank of the starting article
- PageRank of the target article

To show the final results we perform a t-test on the success rate and demonstrate that there is no significant bias.

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

Overall, we can approximate what each member has spent most time on:

- Jason Becker: classifying and explanation of jupyter notebook
- Ruben Jungius: classifying and datastory
- Juan Enrique Martín: initial analysis and datastory
- Pablo Menéndez: classifying and initial analysis
- Jiri Pospisil: initial analysis and observational study

## Sources

Mark Graham (2 December 2009). "Wikipedia's known unknowns". The Guardian.co.uk. Retrieved 12 June 2020. http://www.guardian.co.uk/technology/2009/dec/02/wikipedia-known-unknowns-geotagging-knowledge

David Laniado, Marc Miquel Ribé, "Cultural Identities in Wikipedias", SMSociety '16, July 11 - 13, 2016, London, United Kingdom. https://www.academia.edu/25481875/Cultural_Identities_in_Wikipedias

Hecht, B.J. and Gergle, D. 2010. "On the localness of user-generated content." Proc. CSCW.

Internet Archive. “2007 Wikipedia Selection for schools”. Wikipedia. https://web.archive.org/web/20071006054112/http://schools-wikipedia.org/

Robert West, Jure Leskovec et al. Wikispeedia navigation paths. SNAP: Stanford Network Analysis Platform. https://snap.stanford.edu/data/wikispeedia.html
