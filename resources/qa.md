# Creating QA list
## Objectives
- Create 20 biologically relevant yes/no questions that can be answered using the RDF Portal. 
- Each question must be accompanied by SPARQL queries that provide the answer to the question.
## Procedure
- Use `list_databases()` to find available databases.
- Pick one database of interest.
- Use `get_MIE_file({dbname})` to learn the structure of the database.
- Form a appropriate for the chosen database.
- Construct SPARQL queries, based on the MIE file, corresponding to the question.
- Run the SPARQL queries to validate the results
- Pick another database, possibly redundant, and repeat the process.
- Output the questions, SPARQL queries, and the summary of answers in a Markdown file.


