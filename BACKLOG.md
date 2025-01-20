OpenBook Studio: Development Backlog
====================================

1. [Didactic Considerations](#didactic-considerations)
1. [General Ideas](#general-ideas)

Didactic Considerations
-----------------------

[Conecpt Board](https://app.conceptboard.com/board/gp1k-h2o7-igee-qbh5-z41k?invitationid=ece6433d-432d-4e35-b755-d0366abc0e47)

### Problem Statements

 1. Typical lecture scripts (including the textbooks developed with lecture-slide.js)
    have a rigid, linear structure that is aimed at all learners equally. As a result,
    the individual knowledge level and learning needs of students are not adequately
    taken into account.

 2. As a teacher, I don't know what learning level my students are at and how well
    prepared they are for a particular classroom unit.

 3. As a student, I quickly lose track of what I have to learn by when and what
    content is important.

### Solution Stories

The solution stories are based on typical learning situations over the course of
a semester. Additionally, the need of lecturers to get an overview of their students'
progress is explicitly addressed.

 1. Course Preparation:

    - As a teacher, I would like to be able to define the planned chapters,
      sub-chapters and the associated learning objectives of my lecture in advance.

    - As a teacher, I would like to be able to assign existing teaching materials
      such as scripts in PDF format and HTML textbook pages to the individual chapters.

    - As a teacher, I want to be able to assign my already existing exercises so that
      they can be suggested to learners at the right time or new exercises can be
      automatically derived from them.

    - As a lecturer, I would like to be able to enter the planned lecture dates
      and assign the topics covered. I would also like to be able to assign which
      topics the students should prepare for or follow up on.

 2. Self-study before or after a lecture:

    - As a student, I would like to receive summaries that help me to work on a
      topic in a time-saving manner.

    - As a student, I would like my level of knowledge to be assessed in advance
      so that I can receive suggestions as to what I should learn and how much.

    - As a teacher, I want the students to work on the topics I have set and to
      achieve the minimum learning targets associated with them.

    - As a student, I would like to be offered customised learning nuggets from
      the lecture materials (lecture notes etc.) as well as other materials such
      as videos on a topic. The system should guide me, but allow me to vary the
      order and prioritise topics.

    - As a student, I want to be able to ask questions to clarify unclear issues
      or to explore a topic in greater depth.

    - As a student, I would like various tasks to be generated for me so that I
      can test my knowledge or practise certain aspects.

 3. Learning during a classroom lecture:

    - As a teacher, I would also like to be able to store course materials and
      assignments for use in classroom lessons.

    - In general, as a teacher I would like to be able to use the system in my
      classroom teaching, e.g. in practice sessions.

 5. Learning progress:

    - As a student, I want to know what content will be covered and when, and
      what I need to prepare or follow up on.

    - As a student, I would like to have a skills assessment that gives me an
      indication of the gaps I need to fill.

    - As a teacher, I would like to have an anonymised overview of my students'
      learning progress so that I can adapt my classroom lectures accordingly.
      This should at least show me which units the students have started with and
      which they have already completed. Optionally, I can also see how well they
      have done in these units.

    - As a student, I would like to be able to enquire about the current status
      of the lecture so that I can catch up on the material after an illness.

    - As a student, I would like to be shown the lecture dates from my online
      timetable and be reminded of self-study units that are due.

 4. Exam preparation:

    - As a student, I would like to be given tasks to prepare for exams and have
      my solutions assessed.

    - As a teacher, I want the tasks generated to be based on examples I provide
      and to cover different learning levels of Bloom's taxonomy.

    - As a student, I would like flashcards (and other forms of self-tests) to
      be created for me so that I can test my knowledge.

### User Stories and Quality Stories

General Ideas
-------------

Even though the precursor to OpenBook Studio - lecture-slides.js - has been around
since 2017, development of this successor is still in the very early stages.
The following list contains a few very high-level ideas on what we want to work
in the future in no particular order.

Want to pick up a topic or plan a project with your students? We are looking forward
to hearing from you. Let's get in contact. :-)

* Modern redesign of the old lecture-slides.js library
* Modern redesign of the old ls-xyz plugins (using a light-weight web component framework)
* WYSIWYG online editor to edit textbooks directly in the browser
* Running textbooks directly from the textbook server
* Static export of textbooks for deployment on a static web server / upload in a learning management system
* Import and export of textbooks as ZIP bundles for backups and migration to another server
* Many more content plugins :-)
* Possibility for students to make annotations and notes in the textbook
* Graded learning quizes with server backend (know which student scored in which test)
* Anonymous learning statistics (how many of a course have read which pages?)
