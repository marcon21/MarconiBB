# Testing Document and Plan of MarconiBB
##### Created By: Marcon D. - Strambini E. - Tezza G.

## Introduction

This document outlines the test plan for MarconiBB made by ITI G. Marconi in Verona. As outlined in the project Requirements Document, this system needs to provide an efficient way to allow users to reserve class rooms in the institute ITI G. Marconi Verona. The testing activities discussed in this document will verify that the software for the reservation meets the needs of the customer by verifying that the requirements for this system, as outlined in the Requirements Document, are met.

---

## Items Tested

Items that will be tested during the testing phase as laid out by the Macro Project
Plan will be but are not limited to:

- [ ] Ability for students and professors to use their accounts.
      Test Case: 1.1
- [ ] Ability to reserve a laboratory.
      Test Case: 1.2
- [ ] Ability to reserve a standard room.
      Test Case: 1.3

---

## Approach

The overall method to this testing procedure is manual system testing. Each test
case created will have a direct link to the requirements as laid out in the
Requirements Document. Test cases that include similar Feature methods will
be tested together. Examples of these features include logging in to submit a
question, logging in to submit a survey and/or logging in to the back-end website.
Test cases such as these test the security features of the system along with the
ability to submit information to the database. Each test case will test the security
feature with invalid and valid data (usernames and passwords) to ensure that
user requirement of valid users for these features is met.
The features that specify reading previously asked questions and searching by
keyword will be tested together but in separate test cases. Searching by keyword
through previously asked questions and answers will verify the system’s ability to
produce results that an individual can validate visually.
Manual system testing will continue throughout the second and third iteration of
the project. For each iteration, both old and newly implemented features will be
tested. Adding new features or functionality can sometimes interfere with the
functionality of old features and to ensure product/project success, all features
implemented should function as intended throughout the life of the software.

---

## Item Pass/Fail Criteria

The minimum requirements for this software system were laid out in the
Requirements Document and the Macro Project Plan outlined what the creators
of the software considered project success.
Implemented features that meet the requirements as determined by the
customer, meaning the feature does what the user wants it to do with very little
difficulty, passes the testing procedure. Difficulty, as used here, is determined by
user comprehension and user ability to use the feature with little to no training.
Features that contain major defects will fail the testing procedure and will be
documented via an incident report and turned over to the developer for
investigation and revision.

---

## Test Deliverables

In addition to the Test Plan, other test deliverables include the Test Specification
which outlines the specific test cases and expected results of each test, and Test
reports which is comprised of Incidents, Defects and Changes.

---

## Testing Tasks

The following list the testing deliverables and the activities required to produce
the deliverable.

| Deliverables            | Activities                                                           |
| ----------------------- | -------------------------------------------------------------------- |
| **Test Plan**           | Analyze Requirements for System Features                             |
|                         | Determine Testable/Non-Testable                                      |
|                         | Features Develop Approach/Method for testing                         |
|                         | Determine Task and Estimate Efforts                                  |
|                         | Develop Schedule for Testing                                         |
|                         |                                                                      |
| **Test Specifications** | Analyze Requirements                                                 |
|                         | Define Test Cases for Testable Features as Outlined by the Test Plan |
|                         |                                                                      |
| **Test reports**        | Implement Test Cases as Outlined by the Test Specifications          |
|                         | Document Incidents and Defects                                       |
|                         | Determine Severity of Incidents and Defects                          |
|                         | Determine Changes that Need to be Made to System                     |
|                         | Document and Submit Change Request to Developer                      |
