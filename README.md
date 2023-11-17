### __Title__

GeoWiki

### __Abstract__

As online educational platforms increasingly become vital tools for knowledge dissemination, it is crucial to examine potential biases that may influence user experiences and content representation. For this reason, in this project we aim to investigate the presence of geographical biases in the Wikispeedia game and in the behavior of its players. Wikispeedia is a game where the goal is to get from one article to another by using links, the more someone is aware of potential links between articles, the more likely he/she is to succeed.



Based on the origin of the dataset, the [2007 Wikipedia Selection for schools](https://web.archive.org/web/20071006054112/http://schools-wikipedia.org/), which is targeted for children in the UK, and the origin of Wikispeedia itself (Canada), we want to observe if there is a bias towards the regions of North America and Europe (collectively) in the selection of articles and in the way people play the game.

### __Research questions__

To correctly answer if there is a bias towards Europe and North America (NA) we will propose and answer the following research questions:



-   Are there more articles for Europe and North America than for the other continents?


-   Are there more articles from Europe and NA in the paths than there should be?




We want to conduct an observational study where the treatment group are the games whose paths that end in NA and Europe related articles and the control group the games that end in other continents related articles. Our objective would be to minimize the confounding factors that could bias our analysis so we can analyze paths where the difference is only the goal.



More specific questions:



-   If the article goal is related to a different continent from Europe and NA…


… do people restart the game earlier?

… do people spend more time playing?

… do people take longer paths?



-   Do people tend to back up from articles not related to NA or Europe?


-   Are there more finished paths in percentage for articles that end in Europe?




### __Methods__

**PRE-PROCESSING**

**CLASSIFYING ARTICLES**

In order to classify articles, we first focus on the geographical categories that are predefined in our dataset. By doing this we already get countries, cities and geographical articles from specific continents (Europe, North America, South and Central America, Africa, Asia, Oceania, Antarctica).



Then, we can also get some categories that are specific from one continent like British_History, Monarcs_of_United_Kingdom, America_History or USA_presidents. Once we have done this we look for the names in the articles that contain a country (like Napoleon_I_of_**France),** a city (1755_**Lisbon**_earthquake) or any other geographical name already classified as well as nationalities like British, American or Canadian.



Then, for classifying the rest of the articles we have the following methods:

-   Our first idea was to use the semantic distance between articles and look for the geographical one that was the closest to our article. However, this method was computationally complex and included the article bias we are trying to find.

-   Using weighted links: We calculated the position of the links in the articles and we sort them based on the position assigning more weight to the first links. As we know from before which links are assigned to which continent, the continent with the most sum of weights gets assigned. We already tried it with the People category and we got good results.

-   Analyzing the first paragraph: Just by looking at the information at the beginning of the articles we can get the information of origin as it is normally the first one in the articles.

-   Looking at the whole article: Other idea would be to cluster articles by transforming them to vectors and calculate the distance between them.

-   Category non-continental: There are plenty of articles that are general and could not be assigned to a continent. We can simplify our analysis by setting some categories like Business or Animal Rights to non-continental and some articles that have no links related to nothing geographical as non-continental.




**OBSERVATIONAL STUDY**

After we classified the articles, we will conduct an observational study using a model like in the case of the treated and control case seen in class. We will compare the performance of the players in the treatment and control groups. We define performance as a combination of time of completion, time before restart, and if the path was completed or not. We expect to find a trend indicating that paths leading to topics that can be associated with NA/Europe have a higher play and completion rate due to a knowledge foundation.



As in every observational study, an important step is matching. Some factors to match games can be:

-   Starting article

-   The [PageRank](https://es.wikipedia.org/wiki/PageRank) of the goal (indicates the same probability of reaching the goal). Already computing and in the file pagerank.csv

-   Same category of the goal


### __Proposed milestones for P3 and Timeline__

17.11.2023 - Deliver P2

24.11.2023 - Finish classifying all the articles

04.12.2023 - Finish general analysis of the data classified and start observational study

10.12.2023 - Finish observational study

14.12.2023 - Finish computing all the visualizations needed for Data Story and start with Data Story

20.12.2023 - Finish Data Story

22.12.2023 - Deadline

### __Organization within the team__

At the moment there is no individual organization within members, we work together as a team.

### __Questions for the TA__

-   Which control and treatment group is best to consider?


-   Is it a good idea to conduct other observational analyses? For example, searching for biases for individual continents with different treatment and control groups.