# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
Ans: The system allows a user to enter information about themselves and their pets, schedule tasks for their pets, and display that plan.
- What classes did you include, and what responsibilities did you assign to each?
Ans:
Diagram: Pet Business
Classes: Customer, Pets, Tasks, Plan
Methods: Customer - Add, update, and delete tasks; add, update, and delete user information; be assigned to their pets
Pets - Add, Update, and delete records; Special Instructions
Tasks - Walks, Feeding, Meds, Enrichment, Grooming
Scheduler: Book, Update, and Delete plans, give priorities to tasks

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. One change was adding bidirectional relationships by giving Customer a plans list and Pets a tasks list so objects can be navigated from either side, making it easier to look up a customer's plans and a pet's required tasks while keeping the model consistent with the UML design.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
Priority, duration, time-of-day, completion status, recurrence and time-overlapping conflicts.
- How did you decide which constraints mattered most?
I prioritized constraints that directly affect the feasibility and usefulness of a schedule. Time conflicts and completion status were treated as the highest priority to prevent invalid schedules, while priority, duration, time of day, and recurrence were used to optimize the ordering of tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
One tradeoff is The scheduler using Python's built-in sorting (sort()/sorted()) to order tasks by priority and scheduled time instead of implementing a more specialized algorithm.
- Why is that tradeoff reasonable for this scenario?
Because Pawpal only manages a small number of pet-care tasks, so the simpler, more readable approach provides sufficient performance while being easier to maintain.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
