Excel2DB
========

Create a schema and populate a database from legacy Excel documents.

It currently only uses a baked-in schema, but the intent is that eventually
you will define a schema in models.py, define how it is filled in a template
excel file, and then create a database from that point.

So many places that I have worked have depended on some form of Excel file.
When robust enough, this will allow keeping the history from those files, and 
immediately show the power that comes from having a _real_ database. 
