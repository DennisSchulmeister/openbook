OpenBook: Interactive Online Textbooks
=============================================

1. [Short Description](#short-description)
1. [Didactic Considerations](#didactic-considerations)
1. [Further Documentation](#further-documentation)
1. [Copyright](#copyright)

<p align="center">
   <!-- https://pixabay.com/photos/screwdriver-background-screw-wooden-1008974/ -->
   <img src="_img/under-construction.jpg" alt="Under Construction" width="300">
   <br>
   <b>Under Construction</b>
   <br>
   This is not yet ready for production. Many features are still missing!
   <br>
   Leave a star on GitHub and send us a message to stay updated.
</p>

Short Description
-----------------

OpenBook is the successor to [lecture-slide.js](https://www.npmjs.com/package/@dschulmeis/lecture-slides.js)
which as been in development since 2017. The main idea is still to create beautiful and engaging
online course materials for my students in the form of interactive online textbooks. Because this
is the form that the previous "lecture slides" have taken now (textbooks instead of annotated slides).
Additionally, not only the architecture shall be completely renewed, but many more features are planned:

   * Online WYSIWYG editing of course materials
   * Static export of course materials for LMS upload or static web hosting
   * Many more interactive elements
   * Integration with 3rd party libraries like [H5P](https://h5p.org/)
   * AI-based interactive tutor
   * And many more

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

Further Documentation
---------------------

At the time being there is no full documentation, yet. But README files are available to summarize the
most important points for different target groups:

* [CHANGELOG.md](CHANGELOG.md): Release change log
* [PLANNING.md](PLANNING.md): Planned developments
* [BACKLOG.md](BACKLOG.md): Ideas what could be done
* [HACKING.md](HACKING.md): Information for developers
* [DEPLOYMENT.md](DEPLOYMENT.md): Installation notes for administrators
* [CONTRIBUTORS.md](CONTRIBUTORS.md): List of contributors (patches welcome)
* [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): Our community code of conduct

Copyright
---------

OpenBook: Interactive Online Textbooks <br/>
© 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de> <br>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

Development funded by the KoLLI research project at DHBW Karlsruhe.
