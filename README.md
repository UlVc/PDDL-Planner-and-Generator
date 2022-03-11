# PDDL Planner & Generator

<h4 align="center">A PDDL planner. A PDDL generator.</h4>

## What is PDDL?

**Planning Domain Definition Language** (**PDDL**) is an attempt to standardize [Artificial Intelligence (AI) planning](https://en.wikipedia.org/wiki/Automated_planning_and_scheduling "Automated planning and scheduling") languages. Components of a PDDL planning task:

 - **Objects:** Things in the world that interest us.
 - **Predicates:** Properties of objects that we are interested in; can be either true or false. 
 - **Initial state:** The state of the world that we start in. 
 - **Goal specification:** Things that we want to be true. 
 - **Actions/Operators:** Ways of changing the state of the world.

### Putting all together

Planning tasks specified in PDDL are separated into two files: 

 - A **domain** file for predicates and actions. 
 - A **problem** file for objects, initial state and goal specification.

#### Domain file

Domain files look like this:

    (define (domain <domain name>)
		<PDDL code for predicates>
		<PDDL code for first action>
		[...]
		<PDDL code for last action>
	)
where

 - **`<domain name>`** is a string that identifies the planning domain. 
 
 
#### Problem file

Problem files look like this:

    (define (problem <problem name>)
		(:domain <domain name>)
		<PDDL code for objects>
		<PDDL code for initial state>
		<PDDL code for goal specification>
	)

where

 - **`<problem name>`** is a string that identifies the planning task. 
 - **`<domain name>`** must match the domain name in the corresponding domain file.

## Execution

For executing the program, execute the `__init__` file. For example, if you are inside `src`, execute the command

    python3 __init__.py

On the terminal it will say in which level is exploring the nodes using BFS. After terminating, it will create 3 text files: the domain, the problem, and the actions to take to get to the goal.

## Note

This was the final project for my undergraduate class of AI imparted by [Dra. Verónica Esther Arriola Ríos](https://sites.google.com/view/angeldeplata/). The code for creating PDDL objects were provided. However, the code for the planner (including the BFS algorithm), translation, format improvements and defining both domain and problem was done by myself.
