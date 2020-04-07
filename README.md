IQAS(Intelligent Question Answering System)

IQAS is rule-based, intelligent question answering system build purely using Natural Language Processing Techniques. It extract answers from top google links. I am currently focused on improving the accuracy of the extracted answer.

MODULES REQUIRED

1. Spacy
2. NLTK
3. Wikipedia-API
4. en_core_web_lg
5. BeautifulSoup4
6. Google Search
7. Requests
8. Json
9. Numpy
10. Date-Time
11. String

MODULES INSTALLATION

1. pip install spacy
2. pip install nltk
3. pip install Wikipedia-API
4. !python -m spacy download en
5. !python -m spacy download en_core_web_lg
6. pip install beautifulsoup4
7. pip install google-search
8. pip install requests

REQUIREMENTS

Python version: 3.6 or above

Stanford-corenlp-full-2018-10-05

DATABASE USED

MySQL version: 5.7.29

COMMAND TO CREATE TABLE REQUIRED FOR DATABASE CACHING

"create table <TABLE NAME> ( Id int(11) UNSIGNED NOT NULL AUTO_INCREMENT, Value int(11) UNSIGNED NOT NULL, Answer Text, creationTime datetime DEFAULT CURRENT_TIMESTAMP, modificationTime datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,CONSTRAINT `PK_users` PRIMARY KEY (id))ENGINE=InnoDB;"

\*\* Please enable utf8mb4 through the following instructions. This is required as utf8 only store words of 3 bytes, but sometimes answer contain words of 4 bytes

1. Open my.cnf configuration file of your mysql
2. Copy these commands
   [client]
   default-character-set = utf8mb4

   [mysql]
   default-character-set = utf8mb4

   [mysqld]
   character-set-client-handshake = FALSE
   character-set-server = utf8mb4
   collation-server = utf8mb4_unicode_ci
   init-connect = 'SET collation_connection = utf8mb4_unicode_ci'
   init-connect = 'SET NAMES utf8mb4'

3. Then use this command for the database
   ALTER DATABASE <DATABASE NAME> CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

4. This command for table
   ALTER TABLE <TABLE NAME> CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

TO RUN

1. Install python 3.6 or above
2. Install the packages specified above
3. Download stanford-corenlp
4. Keep the ua_file.txt in the same directory
5. Open command prompt
6. Go to the standford-corenlp directory and run the command `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port [portnumber] -timeout [timeout]`
7. Open new tab in the command prompt and type in "python3 main.py"
8. Input your question
9. Wait for the answer
10. Give feedback
