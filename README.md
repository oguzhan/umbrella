# Umbrella: Minimal ETL framework that runs on AWS Lambda.

### Manifesto.
Many of you probably had read [Your data isn't that big](https://www.chrisstucchio.com/blog/2013/hadoop_hatred.html) if not have a look, it has good points. Startups usually need some time, until they get to the point that they need to setup their 'Big Data Infrastructure'. But until that point, they also need to gather their data and create an environment where their analysts, business developers and data scientists can work at. To be able to get this data into a datawarehouse, there should be an [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) process and building a custom ETL and data pipeline takes a lot of time and resource. While I was doing a research to find out existing open-source alternatives I came across to [DataDuct](https://github.com/coursera/dataduct) and it's simply so good, and exactly solves this problem also for bigger scales. But unfortunately the project doesn't get updated since for a long time. On the other hand there are alternatives like [Luigi](https://github.com/spotify/luigi) but still, if you just want to move data from your Postgres, MySql, MSSQL etc. databases to your datawarehouse, and don't have enough resources, you will probably get stuck.

That's the minimal problem that I attemp to solve with Umbrella. Easy to install and setup custom ETL that helps you to move data from Postgres, MySQL, MSSQL, SQLite etc databases to your Postgres or Redshift datawarehouse (and maybe more).

### How is this going to work ?
There will be two YAML files for configurations. First one is to keep both databases configurations and second one is going to have list of jobs that needs to be run. (see [Jobs](https://github.com/oguzhan/umbrella/blob/master/jobs/jobs.yaml)) There will be three ways of moving data:
* Move : Truncate the target table, load all data from scratch.
* Sync : Compare primary keys and load the data (Inceremental Load)
* Update/Insert: See [UpdateInsert - AWS](http://docs.aws.amazon.com/redshift/latest/dg/t_updating-inserting-using-staging-tables-.html)

Another point of the project is that it should provide Analyst-Friendly Pipeline. That means, when analysts (or data scientists, depending on your team structure) want to add new job to the pipeline, they shouldn't need more than a review from data engineers. To be able to achieve that, analyst should follow this pipeline;

1. Write the SQL that needs to be run on Source Database (see [queries dir](https://github.com/oguzhan/umbrella/tree/master/database/queries))
2. Write or Update the table definiton if necessary. (see [table definitions](https://github.com/oguzhan/umbrella/tree/master/database/table_definitions))
3. Add job specs to jobs.yaml (possibly on S3, see [example job spec](https://github.com/oguzhan/umbrella/blob/master/jobs/jobs.yaml))

and that's it!

### Installation and Setting Up
First idea was creating a Docker Image, and providing YAML configuration guidence for setup. But lately I've been experimenting around with AWS Lambda (have a look at [AWS Lambda, Serverless, API Gateway Article here](http://dchua.com/2016/03/22/writing-a-serverless-python-microservice-with-aws-lambda-and-aws-api-gateway/) and started to think about creating compressed file of the project and using AWS Lambda to also minimize maintenance, scalability aspects.

Tell me what you think please.
