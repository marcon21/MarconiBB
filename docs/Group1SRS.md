# Software Requirements Specification for MarconiBB

##### Created By: Marcon D. - Strambini E. - Tezza G.

## 1 Introduction

### 1.1 Purpose
The purpose of this SRS (Software Requirements Specification) is to describe the development of MarconiBB, a software that allow to book rooms inside the school.

### 1.2 Scope
The scope of our project is to ease the booking of the rooms and laboratories inside the school, with an easy to use and fast solution.

## 2 General Description

### 2.1 MarconiBB Application Enviroment
The MarconiBB application will run on an all-in-one solution based on a microcomputer (RaspberryPI), this will reduce the costs and facilitate the maintenance of the product.

### 2.2 Users
The final users of our application are divided in 2 categories:
- **Teachers**: they'll be able to book rooms and laboratories with no costraints.
- **Students**: because of the changes in the rules inside the insitute students won't be able to book room or laboratories, but in the future they might be able to become users of MarconiBB. 

## 3 Non Functional Requrements

### 3.1 Security Requirements
In order for the user to be able to make use of MarconiBB they will need to be registered in the main database and they must be provided with a unique badge, that allows the identification inside the software.

### 3.2 Documentation
The final product will be released to the public with an step-by-step guide that will be shown wile the user utilize the product.

### 3.3 User Interface (UI)
The UI of MarconiBB has been created with the main objective of being user friendly and easy to learn. It will have a clean and minimal look, with only the necessary information displayed on screen.

## 4 Functional Requirements

### 4.1 Use Case
The main scope for MarconiBB is to make easier for everyone to book a room inside the institute.

* Actors: anyone with a valid badge
* Basic Path: 
   1) The user swipes the badge in the designated area in the terminal
   2) If there are more than one user everyone have to swipe the badge, otherwise the user can select to continue
   3) The user select the day in which he wants to book a room
   4) The user select the starting hour and the ending our of his booking 
   5) The user select between a room or a laboratory
   6) If the user selected a laboratory the system will let the user chose between a pool of rooms that meet his condition, otherwise the room will be randomly selected.
   7) The system will prompt the user with a brief recap of all the information and ask for the final confirm