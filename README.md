Summary
=======
Email is increasingly used as not only a communication tool, but also an
organizational one. Message tagging, folders, header notes, social network
analysis, and other techniques can be used to categorize, organize, and 
apply other predictive elements to new and existing messages.

The goal of this software is to eventually evolve into an email management
assistant, providing suggestions for new message, and also linking back
to older messages which may be relevant to current discussions.

Objectives
==========
* Cluster existing messages using folder structure as a labeled data set.
  * Will also need to include structured metadata such as to, cc, from lists to
start with. How to cluster based on those?
  * Non-trivial words in the subjects should also be considered more strongly
than the body - possibly as labels?
* Produce a graph of the folder corpi, showing the terminology clusters for each

Use Cases
==========
* Suggestions on where to file new messages;
* Identify potentially duplicate folders;
* Identify all the folders where a message may have been 
filed
* Identify messages which have been potentially mis-filed.

Approach / Technologies
=======================
The overall approach is to build a corpus of email text for each folder, capture
the header and other metadata about messages in each folder in a knowledge base,
and then perform multi-variate clustering.

