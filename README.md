# From Table to Heatmap

In Version 0.1 we created simple table display for our progress data. It uses only data directly available on the repository resource. However, from this data we cannot

- directly infer if the latest commit was successful or if just checked out
- only see the actual human users (just relying on splitting repo names is not enough)
- we cannot see the progress over the different sessions and exercises

## Let's do some data wrangling

Our idea: Let's produce a heatmap display from the repository data

Our prototyping approach:

1. Create a data structure with just the necessary info 
2. Get all the necessary data from Github   
3. Find a way to save this data temporarily in a CSV file (instead of proper caching or DBMS)
4. Transform the data into a Pivot Table with Pandas showing Users, Sessions, and Completed Exercises (Absolute/Relative)
5. Display the transformed data in a Seaborn Heatmap

Our Goal: Get a first draft of a working systems which retrieves, stores, transforms, and displays our data in a concise form. Do refactoring and proper OOP later.

### Data Structure

Let's brainstorm which fields we need!


### Data Retrieval

How do we authenticate and store authenticated sessions safely?

### Data Storage

What are our options for storing our data and why?

### Data Transformation

What can we do to prepare (aggregate) our data in view fitting to the Seaborn Heatmap?

### Data Visualization

How can we optimize the heatmap? Absolute values, Tooltips, Links? 


## Reflection

How can we structure the code better?
How can optimize data load time?
What can we improve on the UI?




