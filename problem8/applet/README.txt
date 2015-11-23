Note: index.html must be in the same folder as data.
Course: Heuristic Problem Solving Fall 2010
Title: Dating Game
Architect: Anjali Menon (aam465@nyu.edu)

About the Game:
---------------

Matchmaker M is trying to figure out what kind of person P wants to date. The matchmaker is presented with a set of candidates and chooses the best ones for the person. P will report to M how much P likes those dates (score between -1 and 1, where 1 is good and -1 is very bad). P's criteria for liking a date or not depend on the weights given to various attributes -- e.g. literary knowledge, ability to solve puzzles, and others. The weights may be positive or negative ranging from -1 to 1 and specified as decimal values having at most two digits to the right of the decimal point, e.g. 0.13 but not 0.134.

A candidate C has values for each of n attributes -- each value is either a 0 or a 1. Given the weights P has assigned to each attribute w1, ..., wn and the values C has for each attribute v1, ..., vn, the score P gives to C is simply the dot product of the two vectors. P must set up his or her weights so there is an ideal matching candidate that gets a score of 1 and an anti-ideal candidate that gets a score of -1. No candidate gets a score below -1 or above 1. That is, the sum of P's positive weights is 1 and the sum of the negative weights is -1. 


Score: 
------

Syntax: (best score, number of candidates picked to get to best score).

Single player game: Game over when the matchmaker finds the ideal candidate.

Two player game: The matchmaker to find the ideal candidate first wins.  

In a timed game the winner is the matchmaker who finds the ideal candidate before time runs out or is the matcmaker who has the best candidate score at the end of 120 seconds. If neither matchmaker has found the ideal candidate in 120 seconds and both matchmakers have found candidates with the same best score, then the matchmaker who found their best candidate in the least number of moves wins.


How To Play:
------------

Menu:
* Choose number of matchmakers - one or two
* Choose difficulty level - easy (5 attributes)
			    med (10 attributes)
			    hard (20 attributes)
* Choose timer on/off

Game:
Candidate: The matchmaker(s) is presented with 50 candidates. Toggle between sets of 5 candidates using 'NEXT' and 'PREV' or select one of the colored tabs to pick a specific set of candidates. Each candidate profile includes the candidate name, the set of n attributes and their values. When a candidate is selected the candidate score is displayed at the bottom of that candidate's profile. The score is also displayed on the graph (right hand-side of browser) relative to the ideal candidate score.

Person: The person profile is displayed on the upper left hand corner of the browser. Displays the person's name.

Timer/Score: Displayed on left hand side of browser. 

Win declaration: The win statement is displayed below the candidate profile set.


