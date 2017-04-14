Infection Interview Project
==============

*Author: Andrew Han*

Introduction
--------------
This project implements the Infecton based rollout for slowly adding new feature versions for users.
The project is divided into four main packages: models, infection, visualize, and unit tests.
The main file is to unpack any manual configurations in input.txt to test and run the infection on the data.
The input file is formatted with the first line being the infection options, second line is all members in the graph and every following line is a class setup.

Models
--------------
There are two classes in the models file:
- User
- Graph

**User**
The user model contains infromation about the user on the site, including name, classes taught, classes enrolled, and site version.

**Graph**
The Graph model is the object which represents the connection between users and the classes taught.
It has a dictionary which maps a unique user ID (currently set as its name), and points to the respective user instance.
The classmembers datastructure is a dictionary which maps a class id to the set of users.
The classgraph object contains methods for adding users to the graph, fetching users, and setting relationships between users and classes.

Infection
--------------
The infection package has three main methods for infecting a graph. All of them start with a specific user.
**Total Infection**
- The main idea of a total infection is to infect by class. Since classes connect users, if we recursively infect associated classes, we infect all users.

**Limited Infection**
- Similar to the total infection, we infect by class. However we must choose which classes to infect in order since there is a limit.
- We recursively set a 'class pool' with available classes and we figure out which class to choose to give us the closest infected users to the limit.
- Everytime we decide to infect a class, we must add all other undiscovered classes affiliated with the selected class members to the 'class pool'.

Visualize
--------------
The visualize package is to represent the state of certain data models.
**Teachers**
- Lists all users and what class ID they teach.
**Student**
- Lists all users and what class ID they are a student in.
**Clasrooms**
- Lists all class IDs and the users associated with each class.
**User Versions**
- Displays all users and their site versions.


Unit Tests
--------------
The unit_test.py file as standard tests to see if the implementations work as expected. There are three test classes: TestGraph, TestTotalInfection, and TestLimitedInfection.
TestGraph sets up user and graph models and see if they are properly configured and mapped.
The TestTotalInfection class tests the total infect method on a disconnected, cyclic, and general graph.
The TestLimitedInfection class tests the limited infect method on a general graph from 1 - count of all nodes and checks the anticipated version changes.

Instructions
--------------
To run unit tests execute this command while in the project:
    python unit_test.py

To run manual scenarios and infections, modify the data.txt file.

**Infection Types Enums**
- 1: Total Infection
- 2: Limited Infection

The input will be read as follows:
- 1st line will be the infection command separated by spaces: [infection type enum] [user_name] [new_version] [target_count]
- 2nd line will be the names of the users in the graph, separated by spaces
- Every line following will be the classroom relationships in this format: [teacher] [student1] ... [studentN]

After you have the data set up, run:
    python main.py

The console will show the state of the user graph and the user versions before and after the infection