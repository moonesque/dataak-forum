# Harvesting Project
This projects implements the required task in Python 3, using Scrapy framework.
## Setup
To setup the project, navigate to the root and create a virtual environment.
```
python3 -m venv venv
source venv/bin/actiavte
```
Install the dependencies, using pip:
```
pip install -r requirments.txt
```
Create a MySQL database:
```
CREATE database dataak_forum CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
use dataak_forum;
```
Navigate to the project directory and edit the settings.py file.
```
cd dataak_forum
vim settings.py
```
Modify the ```CONNECTION_STRING``` to match your MySQL credentials.
## Usage
To run the crawler and store the data in the MySQL database:
```
scrapy crawl forum-grab
```
You should now be able to query the database and get the desired result.
 The ```mysqldump``` of the database is included in the root of the project.

The following queries answer question #4 on the given task:

* Users with the most posts:
```
select author, count(id) as posts from posts group by author;
```
* Number of all posts in the whole forum:
```
select count(*) as posts from posts;
```
* Forums with the most active users:
```
select forum, count(author) as active_users from (select author, t.forum from posts as p inner join threads as t on p.thread_id = t.id group by author, t.forum) as sub group by forum order by active_users desc;
```
* Threads with the most active users:
```
select t.thread, count(author) as unique_authors from posts as p inner join threads as t on p.thread_id = t.id group by thread_id order by unique_authors desc;
```
* Forums with no posts:
```
select f.forum, coalesce(t.foo, 0) from forums as f left join (select forum, count(forum) as foo from threads group by forum) as t on f.forum = t.forum;
```
