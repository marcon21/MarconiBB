# Architecture Document for MarconiBB

##### Created By: Marcon D. - Strambini E. - Tezza G.

# Introduction
The purpose of our project is to ease the booking of rooms and laboratories inside the institute, while speeding up the process and save paper.
We use an all-in-one solution, based on a microcomputer that serves as a terminal where the end users can book room. The software is easy to use, fast to learn, with a minimal and eye catching interface.

# Design Goals
The scope of our project is to ease the booking of the rooms and laboratories inside the school, with an easy to use and fast solution.

# Presentation Layer

## Purpose
To display option for the user booking and ease the physical interaction with buttons in the terminal.

## Components
An HTML page will be in charge of displaying appropriate option and reference with the phisical buttons.

# Controller Layer

## Purpose
Allow the page to react in real time to the choices made.

## Components
Flask, a Python library, will be in charge of handling the page response to the user actions and so changing the pages.

# Data Access Layer

## Purpose
This layer is in charge of comunicate to the database and handle the RFID reader and buttons data.

## Components
Python will be in charge of gathering the data from the physical components, processing it first and communicating them next to the controller layer.

# Database Layer

## Purpose
This layer is in charge of storing data in persistent storage.

## Components
PostgreSql will manage data storage and database queries.