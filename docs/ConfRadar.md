# ConfRadar

[Introduction](#introduction)

[Contributions](#contributions)

[Roles](#roles)

[Timeline](#timeline)

[Data](#data)

[Idioms List (Glossary of Terms)](#idioms-list-\(glossary-of-terms\))

[Data Definition](#data-definition)

[Sample Data](#sample-data)

[Retrieval Task](#retrieval-task)

[Task Definition](#task-definition)

[Metrics](#metrics)

[Clustering Task](#clustering-task)

[Task Definition](#task-definition-1)

[Known Number of Clusters (k \= 2 × \#idioms)](#known-number-of-clusters-\(k-=-2-×-#idioms\))

[Unknown Number of Clusters (Dynamic Clustering)](#unknown-number-of-clusters-\(dynamic-clustering\))

[Metrics](#metrics-1)

[Repo](#repo)

[Goals](#goals)

[Core Features/Capabilities](#core-features/capabilities)

[Serving (Integration and Deployment)](#serving-\(integration-and-deployment\))

# Introduction {#introduction}

Researchers and academics often struggle to keep track of rapidly approaching conference submission deadlines and details. Conference information (e.g. Call for Papers dates, venues, etc.) is spread across many websites, mailing lists, and portals, making it time-consuming to manually monitor. Existing community-driven trackers (such as WikiCFP or field-specific deadline aggregators) cover only a small portion of events and are not always up-to-date[\[1\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=there%20are%20only%20a%20handful,having%20only%20a%20few%20centralized). In fact, conference data is highly dynamic – dates and deadlines frequently change (extensions, venue updates, etc.)[\[2\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=metadata%20generated,In%20future). Missing a deadline can mean lost opportunities for submissions; hence an automated solution is needed. **ConfRadar** addresses this need by leveraging an AI-driven agent to continuously gather conference information, extract key dates, detect changes over time, and present the latest data in a convenient format (e.g. Google Docs or Notion pages). This smart agent will reduce manual effort and ensure researchers have the **freshest, most accurate conference deadlines** at their fingertips.

At a high level, ConfRadar will use **Natural Language Processing (NLP)** and information extraction techniques to parse conference announcements. It will employ an *agent-based architecture* (inspired by frameworks like LangChain) so that a Large Language Model (LLM) can actively perform web searches, call tools, and integrate knowledge as needed[\[3\]](https://medium.com/@takafumi.endo/langchain-why-its-the-foundation-of-ai-agent-development-in-the-enterprise-era-f082717c56d3#:~:text=If%20Chains%20are%20the%20assembly,resolution%20time%2C%20and%20AppFolio%20helping). By combining web crawling, NLP extraction, and a knowledge base, the system will automatically maintain a live repository of upcoming conferences and their deadlines. Crucially, ConfRadar will also perform **temporal change tracking** – if a conference deadline is extended or details are updated, the system will detect the change and update the user-facing document accordingly. Each conference is treated as an entity with versioned information, so the agent can maintain a history of changes (e.g. original vs new deadline dates) for transparency. Overall, ConfRadar’s motivation is to streamline academic planning by ensuring no important deadline or update is overlooked.

## **Contributions** {#contributions}

This project will yield several contributions:

·       **Automated Conference Tracking System:** Develop **ConfRadar**, an end-to-end system that automatically retrieves and aggregates conference information (deadlines, venues, etc.) from disparate sources in real time. This goes beyond existing static lists by covering more events and updating continuously[\[1\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=there%20are%20only%20a%20handful,having%20only%20a%20few%20centralized).

·       **NLP-Based Information Extraction:** Implement robust NLP pipelines (using rules and LLMs) to extract structured data (dates, names, locations) from unstructured Call for Papers announcements and web pages. The agent will demonstrate how LLMs can be used to parse webpages into structured records[\[4\]](https://python.langchain.com/docs/tutorials/extraction/#:~:text=In%20this%20tutorial%2C%20we%20will,this%20context%20to%20improve%20performance).

·       **Temporal Change Detection:** Introduce a mechanism for monitoring changes to conference data over time. ConfRadar will track when deadlines shift or new information appears, highlighting changes to users. This feature provides **freshness** of data that manual methods lack, addressing the issue that “information about future events is very susceptible to change”[\[2\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=metadata%20generated,In%20future).

·       **Alias Resolution & Clustering:** Provide methods to automatically **cluster and link related events**, such as grouping workshop events with their parent conference and resolving different names referring to the same conference series. This entity resolution ensures that, for example, "IJCAI 2025" and "International Joint Conference on AI 2025" are recognized as the same event.

·       **User-Friendly Integration:** Deliver the aggregated knowledge in a user-friendly format by synchronizing updates to platforms like Google Docs or Notion. This integration means researchers can view a nicely formatted deadline calendar or table in their daily workspace without manual copying.

In summary, the project will demonstrate a novel combination of agent-driven web mining, NLP extraction, and knowledge management to solve a real-world information management problem for the research community.

## **Roles** {#roles}

**Student (Or Groman):** The MSc student proposing ConfRadar will be responsible for the end-to-end development of the system. This includes conducting background research, designing the architecture, implementing the retrieval and extraction components, and evaluating the system. The student will also manage data collection and the integration with Google Docs/Notion.

**Supervisor (Dr. Kfir Bar):** Dr. Bar will provide guidance on research direction, methodologies, and ensure the project meets academic standards. He will offer expertise in NLP and information systems, help refine the project’s scope, and review progress in regular meetings. The supervisor will also assist in evaluating results and advising on any technical challenges (such as optimizing the agent or improving extraction accuracy).

# Timeline {#timeline}

The project is planned over approximately **6-7 months** and is divided into key phases with milestones:

·       **Month 1-2:** **Literature Review & Design.** Gather requirements and survey related work (conference data sources, existing trackers, LangChain agents, etc.). Finalize system scope and design the high-level architecture and data schema. Define evaluation metrics and success criteria.

·       **Month 2-3:** **Data Source Integration.** Identify target conference data sources (official conference websites, CFP aggregators, APIs) and implement initial web retrieval components. This includes writing crawlers or using APIs to fetch sample pages, and setting up a database or knowledge base structure for storing conference entries.

·       **Month 3-4:** **Extraction Pipeline Implementation.** Develop the NLP extraction module. Start with rule-based parsing for structured content (e.g. scraping “Important Dates” sections) and then integrate an LLM for more complex cases. Use frameworks (e.g. LangChain) to create an **extraction chain** that takes raw HTML/text and outputs structured fields[\[4\]](https://python.langchain.com/docs/tutorials/extraction/#:~:text=In%20this%20tutorial%2C%20we%20will,this%20context%20to%20improve%20performance). Validate extraction accuracy on a small set of known conference pages.

·       **Month 4-5:** **Clustering & Alias Resolution.** Implement the clustering algorithms to group related conference entries. This involves creating the idioms (alias) list and applying clustering to merge duplicates or link workshops to main events. Test the clustering on known examples (using past conference data to see if the same series/events are properly merged). Also, refine the knowledge base to support linking of records (e.g. a workshop record pointing to its parent conference).

·       **Month 5-6:** **Agent Integration & Intelligence.** Integrate all components into the ConfRadar agent. Using an agent framework, allow the system to autonomously perform tasks: e.g., given a high-level goal “update conference list,” the agent will search for new CFPs, extract data, update the knowledge base, and detect changes. Incorporate scheduling so the agent runs periodically (e.g. daily). Start feeding data to the output format (Google Doc/Notion) for testing.

* **Month 6:** **Evaluation & Iteration.** Evaluate the system on a set of upcoming conferences. Measure extraction quality, freshness of updates, and clustering accuracy using the metrics defined. Collect user feedback if possible (e.g. do some researchers find the Notion page useful and accurate?). Based on evaluation, iterate on the extraction rules or clustering method to improve performance. Prepare the final report and project presentation.  
* **Month 7:** **Finalization and Deployment.** Clean up code, finalize documentation, and deploy the agent for real use. This includes ensuring the Google Docs/Notion synchronization is robust (handling credentials, rate limits) and possibly deploying the agent on a server or cloud function for continuous operation. Conclude with writing the MSc project report, detailing the approach, results, and lessons learned.

*(Note: The timeline is approximate and might overlap; e.g., some clustering work may start earlier, or evaluation might run alongside development in an iterative fashion.)*

## **Data** {#data}

### **Idioms List (Glossary of Terms)** {#idioms-list-(glossary-of-terms)}

To avoid ambiguity in this domain, we define key “idioms” (terms) as used in ConfRadar:

·       **Conference Series:** A recurring academic meeting with a constant name or theme, usually held annually or biennially. *Example:* The ACL (Association for Computational Linguistics) conference series has events named ACL 2024, ACL 2025, etc.

·       **Conference Event (Edition):** A specific instance of a conference series, identified by year (and sometimes venue). It has its own dates and deadlines. *Example:* *ACL 2025* is an event in the ACL series, occurring in 2025 at a particular location with its own submission deadline.

·       **Workshop:** A smaller academic event, often attached to a main conference, focusing on a specialized topic. Workshops have their own deadlines and CFPs, but are usually part of a larger conference program. *Example:* a “Workshop on Machine Translation at ACL 2025.”

·       **Deadline:** A due date for submissions or other milestones (e.g., abstract deadline, full paper deadline, notification date). In ConfRadar, “deadline” typically refers to the **submission deadline for papers** unless otherwise specified.

·       **Call for Papers (CFP):** The announcement of a conference or workshop soliciting research submissions. A CFP usually includes important dates, topics of interest, and submission instructions. Many CFPs are posted on conference websites or platforms like WikiCFP.

·       **Alias / Synonym:** Different names referring to the same entity. For conferences, this could be acronyms, abbreviations, or alternative spellings. *Example:* “NeurIPS” and “NIPS” are aliases for the same conference. Alias resolution is the task of recognizing these as one.

·       **Knowledge Base:** In this project, a structured database or store of conference information. It holds entities (conference series, events) with attributes (dates, location, etc.) and possibly relationships (e.g., workshop X is part of conference Y). This knowledge base will be updated by the agent over time.

*(These idioms will be used throughout the proposal to ensure clarity. For instance, “cluster number \= 2 × \#idioms” in the clustering section refers to using the count of known conference series or terms in the idioms list to estimate the number of clusters.)*

### **Data Definition** {#data-definition}

**Data Sources:** ConfRadar will draw on multiple data sources for comprehensive coverage. The primary sources are official conference websites (which often have an "Important Dates" section listing deadlines) and centralized CFP listings. For example, many conferences in computer science announce calls on their own websites and also on platforms like **WikiCFP** or via association websites (ACM, IEEE conference listings). Community-maintained deadline collections (such as **AI Deadlines**[\[5\]](https://aideadlin.es/#:~:text=AI%20Conference%20Deadlines), which is a curated list of AI/ML conference deadlines) provide useful reference data but are updated manually via pull requests[\[5\]](https://aideadlin.es/#:~:text=AI%20Conference%20Deadlines). ConfRadar aims to automate this by directly parsing official sources. Additional inputs may include academic calendars, Google Calendar feeds (some conferences provide .ics files), and mailing list archives. All data will be normalized and stored in a unified format.

**Data Schema:** We will represent each **conference event** as a structured record in the knowledge base. Key fields in the schema include:

·       series\_name – The name of the conference series (e.g., *International Conference on Machine Learning*).

·       short\_name – Common abbreviation or acronym (e.g., *ICML*).

·       year – The year of the event (e.g., 2025). For workshops, this might include the year and main conference reference if needed.

·       title – Full official title of the event (which might combine series name, year, location, etc.).

·       website – URL of the official conference webpage or CFP announcement.

·       **Important Dates:** sub-fields such as:

·       submission\_deadline – Date (and time zone if applicable) of paper submission deadline.

·       abstract\_deadline – Date of abstract submission (if separate from full paper deadline).

·       notification\_date – Date when acceptance notifications are sent.

·       conference\_dates – The start and end dates of the conference event.

·       location – Venue city (and country or "virtual" if online).

·       category – A label indicating if this is a main conference or a workshop (or possibly a journal special issue CFP, etc.).

·       parent\_event – (for workshops) a reference to the main conference it is affiliated with (e.g., link to the series or event ID of the main conference).

·       last\_updated – Timestamp of when this record was last updated by ConfRadar.

Additionally, the knowledge base may maintain a **conference series entity** for each series, which can hold permanent info like typical acronym, field (e.g., AI, systems, etc.), and list of all years/events. Each series could have a persistent ID internally. This separation helps with clustering and alias resolution (the series acts like a cluster representative linking all its yearly events).

### **Sample Data** {#sample-data}

Below is a hypothetical example of how a conference event might be represented (in JSON-like format for illustration):

{  
   "series\_name": "International Conference on Machine Learning",  
   "short\_name": "ICML",  
   "year": 2025,  
   "title": "ICML 2025: International Conference on Machine Learning",  
   "website": "https://icml.cc/2025/",  
   "submission\_deadline": "2024-02-05T23:59:00Z",  
   "abstract\_deadline": "2024-01-29T23:59:00Z",  
   "notification\_date": "2024-04-15",  
   "conference\_dates": "2025-07-17 to 2025-07-23",  
   "location": "Vienna, Austria",  
   "category": "Main Conference",  
   "parent\_event": null,  
   "last\_updated": "2024-01-10T10:00:00Z"  
 }

In this sample, the *ICML 2025* conference has two deadlines (abstract and full submission), a notification date, and the conference dates and location. If there were an associated workshop (say *ICML 2025 Workshop on Federated Learning*), that workshop entry might look like:

{  
   "series\_name": "Workshop on Federated Learning at ICML",  
   "short\_name": "ICML-FL Workshop",  
   "year": 2025,  
   "title": "Federated Learning Workshop at ICML 2025",  
   "website": "https://icml.cc/2025/workshops/federated",  
   "submission\_deadline": "2025-04-10",  
   "notification\_date": "2025-05-01",  
   "conference\_dates": "2025-07-18 (co-located with ICML 2025)",  
   "location": "Vienna, Austria",  
   "category": "Workshop",  
   "parent\_event": "ICML 2025",  
   "last\_updated": "2025-02-20T09:00:00Z"  
 }

Here the parent\_event field links the workshop to its main conference. This demonstrates how data is structured for both main events and sub-events. The actual implementation might use a relational database or graph database – for instance, a graph representation where “ICML 2025” is a node linked to a “ICML series” node, and workshops link to the main event node.

These structured records are what ConfRadar’s retrieval and extraction components will populate. By having a clear schema, we can measure extraction success (did the system correctly fill these fields?) and easily output the information in various formats (tables in a document, calendar entries, etc.).

## **Retrieval Task** {#retrieval-task}

### **Task Definition** {#task-definition}

The **retrieval task** involves discovering and fetching relevant conference information from the web. ConfRadar’s agent will proactively scan known sources and also perform targeted searches to ensure no event is missed. The retrieval process has several facets:

·       **Seeded Crawling:** We will maintain a list of known conferences (especially top-tier series) and their typical websites. For example, if *NeurIPS* is a known series, the agent will periodically check the NeurIPS official site for updates. Many conferences have predictable URLs or dedicated pages each year (e.g., conference2025.org). The agent can construct these URLs or follow links from a series homepage.

·       **Web Search using LLM Agent:** For conferences not in the seed list or new workshops, the agent can perform web searches (through an API or tool) by querying keywords like “\<research field\> conference 2025 deadline” or using the conference name. Using an LLM-enabled agent here can help interpret search results and decide which links to follow. The agent architecture (LangChain or similar) allows the system to do this autonomously: it can take the goal of finding deadlines, then issue search queries, examine results, and follow promising leads[\[3\]](https://medium.com/@takafumi.endo/langchain-why-its-the-foundation-of-ai-agent-development-in-the-enterprise-era-f082717c56d3#:~:text=If%20Chains%20are%20the%20assembly,resolution%20time%2C%20and%20AppFolio%20helping). This is particularly useful for discovering workshops or new conferences announced on social media or university pages.

·       **Content Retrieval:** Once a relevant page is identified (e.g. a Call for Papers page or a conference home), ConfRadar fetches the page content (HTML). It will use an HTTP client or browser automation to handle dynamic pages if necessary. After fetching, the raw text/HTML is handed off to the extraction module.

A challenge in retrieval is the **heterogeneity of sources**. Some conferences list all deadlines on one page, others have PDFs of CFPs, some might only announce via third-party sites. We will incorporate fallback strategies: e.g., if the official site is sparse, look for a WikiCFP entry or an IEEE/ACM listing. In fact, calls are often posted to WikiCFP[\[6\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=match%20at%20L365%20sending%20out,such%20as%20WikiCFP%20or%20EasyChair), which the agent can parse as well.

Another key aspect is **frequency and scheduling**. The retrieval agent will run on a schedule (say daily or weekly) to find new updates. Additionally, we might implement triggers – for example, if an existing deadline passes and no new event for next year is in the system, ConfRadar will specifically search for the next edition's CFP. Over time, the agent “learns” the cycle of conferences (many annual conferences post CFP \~6-9 months before the event date) and can anticipate when to start looking.

Overall, the retrieval task supplies the raw material (texts containing deadlines and details) for the system. By using an intelligent agent approach, ConfRadar’s retrieval is **adaptive**: it can navigate sources and handle different formats rather than relying on a single fixed feed.

### **Metrics** {#metrics}

Evaluating the retrieval task focuses on **coverage, correctness, and freshness** of the information gathered:

* **Extraction Accuracy (Quality):** After retrieval and extraction, we measure how accurately the system captured the relevant information. This can be evaluated by comparing against a ground truth set of conferences. For a sample of conferences, we will manually record the correct deadlines and details, then see if ConfRadar’s output matches. We will use standard information extraction metrics: **precision** (what fraction of the extracted data is correct) and **recall** (what fraction of the relevant data was extracted)[\[7\]](https://www.researchgate.net/figure/Precision-recall-and-F1-measure-for-information-extractors-under-different-levels-of_fig2_282004790#:~:text=,39%5D.). For example, if a page had 5 important dates and the agent extracted 5, but 1 was wrong, precision is 80%; if it missed 1, recall might be 80%, etc. The harmonic mean (F1-score) provides an overall extraction quality measure[\[7\]](https://www.researchgate.net/figure/Precision-recall-and-F1-measure-for-information-extractors-under-different-levels-of_fig2_282004790#:~:text=,39%5D.). High precision means the agent avoids false information; high recall means it finds all the key dates. We expect to tune the system to improve these – for instance, refining the parsing rules or prompt until the LLM reliably picks up all dates and labels them correctly.  
* **Freshness (Timeliness):** This metric evaluates how up-to-date the system’s information is. One way to measure freshness is the time lag between an official update and ConfRadar’s update. For instance, if a deadline change is announced on a website, does our system catch it within 24 hours? We will log timestamps each time a page is checked and when changes are detected. Since it’s hard to get exact ground truth for when an update occurred, we may simulate scenarios (e.g., introduce a known change in a test page at a specific time). The goal is to minimize latency — ideally, ConfRadar updates within a day of any change (or faster if run more frequently). We can also measure the **update frequency**: how often the agent refreshes data and ensure it’s appropriate (e.g., daily checks for nearing deadlines, weekly for far-future events).  
* **Coverage:** Although hard to quantify absolutely, we will approximate coverage by focusing on a domain (e.g., major AI conferences in 2025\) and check how many of those are captured by ConfRadar versus how many exist. For example, using an external list of top conferences as reference, if there are 50 relevant conferences and our system found 45, coverage is 90%. We’ll aim for high coverage in the targeted domains (like all *Conferenceranks.com* top conferences[\[8\]](https://github.com/paperswithcode/ai-deadlines#:~:text=Contributions%20are%20very%20welcome%21)). Lower coverage might indicate the need to add more seed sources or improve search queries.  
* **Error Rate:** This is essentially 1 \- precision in extraction, but also includes retrieval mistakes like picking up a wrong date (e.g., a workshop deadline mis-identified as the main conference deadline) or even pulling in a fake/cancelled conference. We will manually review output to ensure the system isn’t picking up **false positives** (like predatory conferences or outdated events). The system’s design (focusing on reputable sources) will mitigate this, but it’s a point of evaluation.

In summary, success for the retrieval task means ConfRadar finds the vast majority of relevant conferences and their deadlines (high recall), with very few errors in the extracted details (high precision), and it keeps the information updated promptly (freshness). For instance, if an evaluation after a few months shows the agent consistently maintains an accurate list of deadlines that is at most 1-2 days behind any official changes, that would demonstrate the effectiveness of the retrieval and extraction components.

## **Clustering Task** {#clustering-task}

### **Task Definition** {#task-definition-1}

The **clustering task** in ConfRadar refers to organizing and disambiguating the collected conference data. There are two primary clustering sub-tasks: **alias resolution** and **workshop grouping**. Both are crucial for presenting clean, unified information to users.

* **Alias Resolution (Conference Name Clustering):** Conferences are often referred to by multiple names or acronyms. For example, *“ICML 2025”* might also appear as *“International Conference on Machine Learning 2025”* or just *“ICML’25”*. The system must recognize these as the same event and avoid listing them separately. We treat each unique string (name) we encounter as an item that might belong to a cluster representing the underlying conference series or event. The clustering task will group these aliases together. This can be approached as an unsupervised clustering problem based on textual similarity and known patterns. We will compile an **idioms list** of known aliases (from our data glossary and external knowledge), e.g., mapping “NeurIPS” \<-\> “NIPS” or “AAAI” \<-\> “Association for the Advancement of AI”. Initially, straightforward rules (string normalization, acronym detection) can catch many aliases. For more complex cases, we can use embedding-based similarity (turn names into vector representations and cluster those). The outcome is that all names in one cluster are considered one entity. This corresponds to merging duplicate entries in the knowledge base – effectively, creating a unique identifier for the conference series and linking all variations to it[\[9\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=will%20have%20to%20be%20amended,only%20one%20PID%20assigned%2C%20indexing)[\[10\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=Another%20reason%20why%20PIDs%20would,any%20duplicates%20in%20their%20database).  
* **Workshop Grouping:** Workshops often have titles that do not explicitly include the main conference name, yet they should be associated with their parent conference. For example, *“Workshop on Computer Vision for Agriculture 2025”* might be a workshop at CVPR 2025, but the title alone doesn’t say “CVPR”. The clustering here aims to connect such workshops to the main conference cluster. We can utilize clues like the workshop’s dates and location – if they coincide or fall within the main conference dates and venue, that’s a strong indicator. Another clue is the workshop website or CFP often mentioning the main event. The agent, when extracting data, could note text like “held in conjunction with CVPR 2025”. We will parse such mentions to assign a parent\_event. In cases where the link isn’t obvious from text, clustering algorithms can group by similarity in timing/location. Essentially, we’ll cluster events that occur at the same place and time as likely related. This grouping prevents the system from listing a workshop as if it were an unrelated conference, and instead nest or tag it under the main conference.

To perform these tasks, we will experiment with two scenarios: when the number of clusters (distinct conferences/series) is known or estimated, and when it’s not known.

#### **Known Number of Clusters (k \= 2 × \#idioms)** {#known-number-of-clusters-(k-=-2-×-#idioms)}

If we have an estimate of how many distinct groups we expect, we can use a **hard clustering** approach like k-means or k-medoids on name embeddings. For instance, suppose our idioms list or initial data suggests \~50 distinct conference series of interest; we might set *k \= 2 × \#idioms* (which provides some buffer allowing workshops or aliases to form sub-clusters). The factor 2 is somewhat heuristic – it acknowledges that our idioms list might not be exhaustive or that we expect roughly twice as many distinct “names” (including workshops) as there are core conferences. Under this approach, we convert each event name into a numeric feature representation. Features could include bag-of-words of the title, TF-IDF of terms, or even use pre-trained language model embeddings that capture semantic similarity (so that “Intl. Joint Conf. on AI” and “IJCAI” end up close in vector space). Then, using k-means with k=2×N, the algorithm will partition the names into clusters. We will then interpret those clusters – ideally, each cluster corresponds to one conference series (with maybe separate clusters for workshops vs main events if the algorithm splits them). We may adjust k or merge clusters based on domain knowledge. This semi-supervised approach leverages an initial guess of cluster count to guide the algorithm.

Using a known k can simplify evaluation as well: we can check if each predefined conference series mostly maps to a single cluster. If not, we adjust features or increase k. The number “2 × \#idioms” is a starting point; it can be refined. The rationale is to allow the algorithm to distinguish cases like main conference vs workshop if needed (two clusters for what a human might consider one group, which we can later link together hierarchically).

#### **Unknown Number of Clusters (Dynamic Clustering)** {#unknown-number-of-clusters-(dynamic-clustering)}

In an open-world scenario, we might not know how many distinct conferences will appear (especially as the agent discovers new events). In this case, we will use **clustering algorithms that determine the number of clusters automatically or use threshold-based clustering**. One approach is hierarchical agglomerative clustering: we start with each name as its own cluster and then merge clusters based on a similarity threshold. For example, we define a similarity score between any two event names (using lexical similarity or embedding cosine similarity). If the score is above a certain threshold (e.g., the names are 90% similar or one contains the other), we merge them. This can naturally handle unknown cluster counts – we stop merging when no pair exceeds the threshold. Another approach is DBSCAN (Density-Based Spatial Clustering of Applications with Noise), which groups points (name embeddings) that are within a distance epsilon. DBSCAN does not need a preset number of clusters; it will form as many clusters as the data suggests, and can leave very unique outliers as singletons (which is fine, maybe a one-off workshop series). We will tune the similarity threshold or epsilon parameter by testing on known alias examples: e.g., ensure “AAAI” and “AAAI-24” cluster together, but unrelated names do not cluster.

Additionally, for alias resolution, we might implement specific rules (like stripping year numbers and seeing if the remaining parts match) as a pre-processing step. For workshops, as mentioned, using metadata (dates, location) is like clustering on attributes – events sharing attributes get linked. This is essentially an **entity resolution** problem, for which a combination of rules and clustering algorithm results can be used. If the algorithm says two names are similar and, in addition, they share a location and date range, we are very confident to merge them. Conversely, if two events have similar names but different fields or times (like “AI for Healthcare Workshop” could happen at multiple conferences), we rely on context to distinguish them.

The output of the clustering task will be a structured linking: each conference series (or cluster) will have a canonical name and list of aliases, and each workshop will be attached to its main conference cluster. This mirrors efforts in research to disambiguate entities; for example, introducing persistent IDs for conferences to avoid confusion[\[9\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=will%20have%20to%20be%20amended,only%20one%20PID%20assigned%2C%20indexing)[\[10\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=Another%20reason%20why%20PIDs%20would,any%20duplicates%20in%20their%20database). Here we achieve a similar outcome through automated clustering.

### **Metrics** {#metrics-1}

To evaluate the clustering and alias resolution, we will use metrics from cluster analysis and entity resolution:

* **Cluster Purity and Inverse Purity:** These measures assess how “clean” each cluster is (purity: the fraction of a cluster’s members that truly belong to the same real conference) and how complete (inverse purity or coverage: the fraction of all names of a real conference that are captured in a single cluster). In our case, we can create a test set of known aliases/groups (for example, we know that {“NeurIPS”, “NIPS”, “Conference on Neural Information Processing Systems 2025”} are all one group). After running clustering, we check each such group: ideally, they end up in one cluster (high inverse purity) and that cluster doesn’t contain names from other conferences (high purity). We will compute purity for each cluster and average, or use an F1-like combination.  
* **Adjusted Rand Index (ARI):** This is a standard metric for comparing clustering results to a ground truth partition[\[11\]](https://oecd.ai/en/catalogue/metrics/adjusted-rand-index-ari#:~:text=Website). It considers all pairs of items and measures how many pairs are correctly grouped vs incorrectly, adjusting for chance grouping. We will use ARI to compare our algorithm’s clusters against the ground truth alias groupings that we have assembled for evaluation. An ARI of 1.0 means perfect clustering (every alias pair that should be together is, and no incorrect pairings). ARI \= 0 would mean essentially random clustering[\[11\]](https://oecd.ai/en/catalogue/metrics/adjusted-rand-index-ari#:~:text=Website). We aim for ARI close to 1 on the evaluation set. For example, if we have 100 conference names in the test and cluster them, ARI will tell us overall how well we did. This metric is useful because it accounts for both precision and recall of clustering decisions in one number.  
* **Pairwise Precision/Recall (for entity resolution):** We can also frame alias resolution as identifying which names refer to the same conference. Then evaluate it like an information extraction task: precision \= (correctly identified alias pairs) / (all alias pair links made by system); recall \= (correctly identified alias pairs) / (all true alias pairs). This is equivalent to how ARI is derived but sometimes easier to interpret. For instance, if our system mistakenly clusters an unrelated conference name in with another, that’s a false positive (hurts precision). If it fails to link an alias that should be linked, that’s a false negative (hurts recall). High precision means every cluster the system makes is usually truly a single conference. High recall means it found links for most of the true aliases. We will likely ensure near-100% precision by using conservative rules (we prefer missing a link over merging two different conferences, as merging would confuse the data). Then we will try to boost recall by incrementally relaxing thresholds until just before precision would drop noticeably.  
* **Manual Evaluation of Grouping:** For workshop-to-conference grouping, we might do a manual check because ground truth can be tricky (not all workshops clearly state their parent). We’ll review a sample of workshop entries and confirm if ConfRadar correctly attached them to the right main conference. Any errors (like linking a workshop to the wrong conference or failing to link at all) will be noted. This qualitative measure will guide adjustments to the grouping logic (for example, if a workshop title didn’t contain the main conference name and our algorithm missed it, we might add a rule to use date/location matching).

The clustering task’s success criteria are that **each real-world conference series corresponds to one cluster in our system, and each cluster corresponds to a single real-world conference or series** (one-to-one mapping), and that workshops are correctly associated. In practical terms, when the data is presented to the user, they should not see duplicate listings for what is actually the same conference. By evaluating with the above metrics, we ensure ConfRadar’s output is both accurate and user-friendly, avoiding the confusion of scattered or duplicated entries.

*Figure: High-level architecture of ConfRadar.* The system consists of an **LLM-powered agent** that orchestrates several components. First, a retrieval module gathers raw content from conference websites and CFP postings. Next, an NLP/Extraction module (which may utilize both rule-based parsing and LLM prompts) extracts structured information (dates, locations, etc.) from the unstructured text[\[4\]](https://python.langchain.com/docs/tutorials/extraction/#:~:text=In%20this%20tutorial%2C%20we%20will,this%20context%20to%20improve%20performance). The extracted data is stored in a knowledge base, where a **change detection** component monitors for updates to any field. A clustering module runs in parallel to link related entries (alias resolution and grouping of workshops). Finally, when new or changed data is confirmed, the system’s serving module updates the user-facing documents (Google Doc, Notion) to reflect the latest information. This architecture enables continuous, autonomous tracking and updating of conference deadlines.

## **Repo** {#repo}

The project’s source code will be managed in a version-controlled repository (Git). A GitHub repository (tentatively named **“ConfRadar”**) will be created for development. This repo will contain all code (crawlers, extraction scripts, agent prompts, etc.), documentation, and sample data. It will also track issues and feature progress. Using Git not only provides backup and collaboration capabilities but also allows for integration with CI tools if needed (for example, to run periodic tests or format the output). The repository will be made available to the supervisor and, upon project completion, can be open-sourced to benefit the community.

Additionally, the repo will include configuration or API keys (secured via environment variables) for services like Notion or Google Docs API. Instructions for setting up those integrations will be documented in the README. By the end of the project, the repository will serve as a comprehensive package for ConfRadar – enabling others to deploy their own instance if desired.

## **Goals** {#goals}

The overarching goal of ConfRadar is to **simplify and automate the monitoring of academic conference deadlines and information**. Breaking this down, the specific goals are:

·       **High Recall of Relevant Conferences:** Ensure that the system tracks a broad and comprehensive set of conferences in the chosen domains (e.g., all major CS conferences), minimizing the chances of missing an important event. This means expanding coverage beyond what a single person might manually track, leveraging the agent’s capability to discover new calls.

·       **Accurate and Timely Information:** Provide information that users can trust. The dates and details listed by ConfRadar should be correct (matching official sources) and updated in a timely fashion when changes occur. The aim is that users will rely on ConfRadar as a **single source of truth** for deadlines, confident that it’s up-to-date.

·       **User-Friendly Delivery:** Present the data in a format that integrates into researchers’ workflows. By populating a Google Doc, Notion page, or similar, the goal is to eliminate the need for users to visit multiple websites or manually compile deadlines. The information should be clearly formatted (e.g., tables by date or conference, possibly with countdowns or highlights of upcoming deadlines) so that it’s immediately useful for planning.

·       **Demonstration of AI Agent Utility:** From a technical perspective, a goal is to demonstrate how a LangChain-style agent can automate web-based tasks (like finding and extracting information) that traditionally required manual effort. The project will showcase the agent’s decision-making – for example, deciding which tool to use (web search vs. direct URL fetch) or rephrasing queries until the needed data is found. This contributes knowledge on using LLM agents for information gathering tasks.

·       **Maintainability and Extensibility:** Design ConfRadar such that it can be easily extended to other domains or maintained with minimal effort. A goal is that adding a new conference series or adapting to a new field (say, tracking grant deadlines or journal special issue deadlines) would be straightforward. This will be achieved by having a clean separation of concerns (modular design) and using configuration files (for known conferences, aliases, etc.) that can be updated without changing core code.

By meeting these goals, the final project will not only solve the immediate problem for the student/researchers at hand (never missing a conference deadline), but also provide a framework that could be reused or expanded for other information tracking challenges.

## **Core Features/Capabilities** {#core-features/capabilities}

ConfRadar’s core functionality can be summarized by its key capabilities, each corresponding to a component in the system architecture:

* **Automated Web Extraction:** The ability to automatically fetch conference information from the web. This includes the agent’s integrated web browser/search tool, which can navigate to conference pages and scrape content. Unlike static scrapers tied to one site, ConfRadar’s agent can adapt to different page layouts by using the LLM’s understanding. For example, it can locate an “Important Dates” section in a page even if the HTML structure varies. We leverage LangChain’s tool use to have the LLM find these relevant sections and extract structured info[\[12\]](https://medium.com/@takafumi.endo/langchain-why-its-the-foundation-of-ai-agent-development-in-the-enterprise-era-f082717c56d3#:~:text=prompt%20goes%20in%2C%20a%20response,magic%20to%20reliable%2C%20structured%20logic). This dynamic extraction is a core feature that ensures generality across conferences.  
* **LLM-Assisted Information Extraction:** A distinguishing capability is using a Large Language Model to parse and interpret text. Rather than writing a separate parser for each site, we provide the LLM with extraction prompts and even a schema definition (e.g., via Pydantic or function calling) to fill in fields. Recent developments allow chat models to output JSON following a given schema[\[13\]](https://python.langchain.com/docs/tutorials/extraction/#:~:text=First%2C%20we%20need%20to%20describe,to%20extract%20from%20the%20text)[\[14\]](https://python.langchain.com/docs/tutorials/extraction/#:~:text=Let%27s%20create%20an%20information%20extractor,the%20schema%20we%20defined%20above). ConfRadar will use this to get structured data (dates, names) from raw text. The LLM can handle date formats, time zones (“AoE” vs local time), and even infer missing year if not stated (using context like the page title or current date). This significantly reduces engineering overhead and increases robustness to format changes.  
* **Knowledge Base with Versioning:** ConfRadar maintains a **knowledge base** of conferences, essentially a mini knowledge graph. A core feature is that every piece of data is stored with context and timestamp. If a deadline changes, the system doesn’t just overwrite it blindly; it can keep a history (previous deadline X was updated to Y on Date Z). This versioning allows the agent to detect changes (comparing new scraped data with the stored data) and to inform users about changes (“Deadline extended from Jan 10 to Jan 17”). Moreover, the knowledge base can be queried: e.g., “find all conferences in April 2025” or “what is the deadline for NeurIPS this year?”. While such query interface is not the primary goal, structuring the data enables these possibilities. Importantly, having a centralized store means the agent’s operations (crawling, extraction) populate a single source that the output generator and clustering module draw from, ensuring consistency.  
* **Temporal Change Detection & Alerts:** Built on the knowledge base, ConfRadar continuously monitors for changes. The system will compare each fetched page’s new content to what was previously recorded. For instance, it might hash or canonicalize the important dates section and see if it has changed. If a change is detected, the agent marks that record as updated and triggers the output sync. The user might see an alert or highlight (e.g., the text in the Google Doc could be color-coded or annotated like “(extended)” next to a deadline). Change detection is not trivial because websites might have minor text changes or updates unrelated to deadlines. We plan to focus on changes in date strings or the addition/removal of dates. This feature ensures that **freshness** is maintained automatically. As noted in literature, keeping up with frequent changes is challenging if done manually[\[2\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=metadata%20generated,In%20future), so this automated change detection is a significant capability of ConfRadar.  
* **Alias & Duplicate Resolution:** As discussed, ConfRadar will actively resolve different references to the same event. This feature manifests to the user as a clean list with no duplicates. Under the hood, it means the system, when adding a new entry, checks against existing ones (using the clustering logic) to see if it’s actually the same event. If so, it merges or updates the existing record instead of creating a new one. For example, if our agent finds “International Joint Conference on Artificial Intelligence (IJCAI) 2025” on one site, and “IJCAI-25” on another, it will recognize these refer to the same conference and unify them. By providing this, we avoid the confusion of one conference appearing twice with slightly different names. It also helps in accumulating all info (maybe one source had the deadline, another had the venue – the merged record will have both). This capability is akin to how reference databases like DBLP try to consolidate conference names, or how the PID (persistent identifier) approach would give one ID to each conference series[\[15\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=%28WikiCFP%2C%20GND%2C%20etc,enter%20conference%20metadata%2C%20would%20make)[\[16\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=keeping%20its%20metadata%20up,unfeasible%20task%20for%20indexing%20systems). ConfRadar does this in an automated way via clustering and heuristics.  
* **Workshop Integration:** A core feature from the user perspective is that workshops are not treated as separate unrelated conferences. Instead, they are contextually integrated. In the output (Doc/Notion), we might present workshops indented under the main conference or tagged accordingly. This way, a user sees the whole picture: e.g., *CVPR 2025 – Paper Deadline: Nov 2024; Workshops: see below (list of workshops with deadlines)*. This feature relies on the successful grouping and also on our output formatting. It’s valuable because many researchers decide on workshops after knowing conference acceptances; having them together in one place aids planning.  
* **User Interface and Sync:** While ConfRadar’s “UI” is essentially the Google Doc or Notion page, designing the output format is a key capability. We plan to have a clear, readable table or database view. For example, on Notion, we can use a table with columns: Conference | Deadline | Notification | Event Dates | Location | Last Updated. Users can filter or sort by date. On Google Docs, we might present by chronological order of deadlines, grouped by month or by field. The **sync** capability means any time the knowledge base updates, these documents update. This could be implemented by writing to the Notion API (which will update a page in real-time) or regenerating a section of a Google Doc via the Docs API. Essentially, ConfRadar serves as a backend and the doc/notion as the front-end. The user doesn’t need to run anything; they just open the document to see current info. Realizing this synchronization reliably (perhaps with periodic pushes or webhooks) is a core part of the serving capability (described below).  
* **Extensibility to Calendars and Alerts:** Beyond the current scope, it’s worth noting that the structured data could easily feed into Google Calendar or email alerts. Though optional, we consider providing an .ics calendar export (similar to existing deadline sites[\[17\]](https://aideadlin.es/#:~:text=Deadlines%20are%20shown%20in%20America%2FNew_York,website%20timezones%2C%20click%20on%20them)) so users can import conference deadlines into their calendars. This underscores that once ConfRadar has the data, it can serve it in multiple convenient ways.

In implementation terms, these features come together using an agent framework: the **LangChain agent** will manage the decision logic (when to search, when to parse, etc.), providing “reliable AI agent” behavior[\[18\]](https://www.langchain.com/#:~:text=LangChain%20LangChain%20provides%20the%20engineering,and%20deploy%20reliable%20AI%20agents), and the modular components (web scraper, parser, database, clusterer) carry out the specialized tasks. By focusing on these core capabilities, we ensure ConfRadar is effective and user-centric in tracking conference deadlines.

## **Serving (Integration and Deployment)** {#serving-(integration-and-deployment)}

The final step is making ConfRadar’s outputs available to end users (researchers, students, or anyone interested in the conference deadlines). The project specifically targets integration with **Google Docs or Notion**, as these are commonly used for sharing and organizing information in academia.

**Google Docs Integration:** One approach is to have a Google Doc that acts as a living document of conference deadlines. Using the Google Docs API, ConfRadar can programmatically insert or update content in the document. For example, the Doc could have a section per year or per quarter, listing conferences and their deadlines. When the agent runs and finds new info, it could update a specific table cell or add a new paragraph. We might structure the doc as a table for easier updates (each row a conference). The serving module will handle authentication (via Google’s API credentials) and then perform the necessary write operations. A challenge here is idempotence – ensuring that we update existing entries rather than duplicating. We can embed hidden identifiers or use unique conference names as keys to find and replace text in the doc. Google Docs integration is appealing because many users are comfortable with Docs and can add their own notes or highlights on top of the auto-generated content.

**Notion Integration:** Notion offers a powerful API and a database model that suits our needs. We can create a Notion **database** with predefined columns (Conference Name, Deadline, Dates, etc.). ConfRadar can then upsert entries in this database. Notion will automatically display them in a table or board view. The advantage of Notion is that it’s very interactive – users can filter by field, or link to other Notion pages. The agent will use the Notion API (with an integration token) to add new conference entries and update existing ones (by unique IDs). Notion’s API is asynchronous, but we can ensure after each agent cycle that the Notion page reflects the knowledge base state.

**Synchronization Frequency:** The serving component will likely run after each major update cycle of the agent (say the agent does a crawl+extract pass, and then pushes updates). Alternatively, for near real-time updates, we could use a **push model**: whenever a change is detected in the knowledge base, immediately call the doc/notion API to update. The frequency can be configured; a reasonable default is to update the public page daily with any new info. Because both Google Docs and Notion maintain version history, any changes ConfRadar makes are logged, and one can even see what changed (which aligns with our emphasis on change detection and transparency).

**Format and Presentation:** We will put thought into how the information is presented. For instance, upcoming deadlines could be highlighted in red if they are within one week, to draw attention. We might sort the list by deadline date by default. We might also provide a section for recently passed deadlines (so users know what just closed). The serving layer can manage multiple views: e.g., separate pages for different research areas (if we categorize conferences by field, like AI, Systems, Theory, etc., each could be its own section or Notion database view). However, initially the focus is a single comprehensive list.

**Deployment:** The agent and serving components will likely run on a cloud platform or a server. We could deploy the agent as a scheduled cloud function or a small server (perhaps on AWS, GCP, or even a Raspberry Pi for personal use). The deployment will be set to trigger at defined intervals. Alternatively, if we integrate with something like GitHub Actions, we could schedule the agent to run via CI and then commit updated data (though updating external services like Notion directly is cleaner). The deployed service will need proper credentials management (API keys for Google/Notion, OpenAI key for LLM, etc.) and error handling (e.g., if an API call fails, try again or log gracefully).

**User Access:** Finally, the Google Doc or Notion page can be shared with the intended audience (could be public or within a group). For a Google Doc, we might set it as viewable by anyone with the link. For Notion, we can publish the page or invite users. In both cases, the result is that users don’t run any code – they simply consult the page. This fulfills the project’s aim of being *user-friendly*. The page essentially becomes a dashboard updated by the ConfRadar backend.

In terms of evaluation of serving: we will test that updates propagate correctly (e.g., if we manually change a deadline in the DB, does the doc reflect it after the next sync?). We will also consider performance – updating a Notion database with hundreds of entries might be slower, but still acceptable if done in seconds or a couple of minutes. We can optimize by only updating changed entries rather than rewriting everything each time.

To summarize the serving plan: **ConfRadar will run as a background service** and **publish live conference information to a collaborative document platform**. This marries the automation power of the agent with the accessibility of tools researchers already use daily. By the end of the project, a user should be able to bookmark a Notion page or Google Doc and trust that whenever they open it, it’s up-to-date with the latest conference deadlines, courtesy of ConfRadar.

---

[\[1\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=there%20are%20only%20a%20handful,having%20only%20a%20few%20centralized) [\[2\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=metadata%20generated,In%20future) [\[6\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=match%20at%20L365%20sending%20out,such%20as%20WikiCFP%20or%20EasyChair) [\[9\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=will%20have%20to%20be%20amended,only%20one%20PID%20assigned%2C%20indexing) [\[10\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=Another%20reason%20why%20PIDs%20would,any%20duplicates%20in%20their%20database) [\[15\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=%28WikiCFP%2C%20GND%2C%20etc,enter%20conference%20metadata%2C%20would%20make) [\[16\]](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf#:~:text=keeping%20its%20metadata%20up,unfeasible%20task%20for%20indexing%20systems) Persistent Identification for Conferences

[https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf](https://datascience.codata.org/articles/1400/files/submission/proof/1400-1-10324-4-10-20220406.pdf)

[\[3\]](https://medium.com/@takafumi.endo/langchain-why-its-the-foundation-of-ai-agent-development-in-the-enterprise-era-f082717c56d3#:~:text=If%20Chains%20are%20the%20assembly,resolution%20time%2C%20and%20AppFolio%20helping) [\[12\]](https://medium.com/@takafumi.endo/langchain-why-its-the-foundation-of-ai-agent-development-in-the-enterprise-era-f082717c56d3#:~:text=prompt%20goes%20in%2C%20a%20response,magic%20to%20reliable%2C%20structured%20logic) LangChain : Why It’s the Foundation of AI Agent Development in the Enterprise Era | by Takafumi Endo | Medium

[https://medium.com/@takafumi.endo/langchain-why-its-the-foundation-of-ai-agent-development-in-the-enterprise-era-f082717c56d3](https://medium.com/@takafumi.endo/langchain-why-its-the-foundation-of-ai-agent-development-in-the-enterprise-era-f082717c56d3)

[\[4\]](https://python.langchain.com/docs/tutorials/extraction/#:~:text=In%20this%20tutorial%2C%20we%20will,this%20context%20to%20improve%20performance) [\[13\]](https://python.langchain.com/docs/tutorials/extraction/#:~:text=First%2C%20we%20need%20to%20describe,to%20extract%20from%20the%20text) [\[14\]](https://python.langchain.com/docs/tutorials/extraction/#:~:text=Let%27s%20create%20an%20information%20extractor,the%20schema%20we%20defined%20above) Build an Extraction Chain | ️ LangChain

[https://python.langchain.com/docs/tutorials/extraction/](https://python.langchain.com/docs/tutorials/extraction/)

[\[5\]](https://aideadlin.es/#:~:text=AI%20Conference%20Deadlines) [\[17\]](https://aideadlin.es/#:~:text=Deadlines%20are%20shown%20in%20America%2FNew_York,website%20timezones%2C%20click%20on%20them) AI Conference Deadlines

[https://aideadlin.es/](https://aideadlin.es/)

[\[7\]](https://www.researchgate.net/figure/Precision-recall-and-F1-measure-for-information-extractors-under-different-levels-of_fig2_282004790#:~:text=,39%5D.) Precision, recall and F1 measure for information extractors under... | Download Scientific Diagram

[https://www.researchgate.net/figure/Precision-recall-and-F1-measure-for-information-extractors-under-different-levels-of\_fig2\_282004790](https://www.researchgate.net/figure/Precision-recall-and-F1-measure-for-information-extractors-under-different-levels-of_fig2_282004790)

[\[8\]](https://github.com/paperswithcode/ai-deadlines#:~:text=Contributions%20are%20very%20welcome%21) GitHub \- paperswithcode/ai-deadlines: :alarm\_clock: AI conference deadline countdowns

[https://github.com/paperswithcode/ai-deadlines](https://github.com/paperswithcode/ai-deadlines)

[\[11\]](https://oecd.ai/en/catalogue/metrics/adjusted-rand-index-ari#:~:text=Website) Adjusted Rand Index (ARI) \- OECD.AI

[https://oecd.ai/en/catalogue/metrics/adjusted-rand-index-ari](https://oecd.ai/en/catalogue/metrics/adjusted-rand-index-ari)

[\[18\]](https://www.langchain.com/#:~:text=LangChain%20LangChain%20provides%20the%20engineering,and%20deploy%20reliable%20AI%20agents) LangChain

[https://www.langchain.com/](https://www.langchain.com/)

