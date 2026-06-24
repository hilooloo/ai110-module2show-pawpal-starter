# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

## Core Actions
1. Add a new pet to the system.
2. Schedule a care task for a pet.
3. View today's tasks sorted by time.

### Building Blocks
- **Owner**
  - Attributes: `name` (str), `pets` (dict)
  - Methods: `add_pet()`, `get_all_tasks()`
- **Pet**
  - Attributes: `name` (str), `species` (str), `tasks` (list)
  - Methods: `add_task()`
- **Task**
  - Attributes: `description` (str), `time_str` (str), `frequency` (str), `is_completed` (bool)
  - Methods: `mark_complete()`
- **Scheduler**
  - Methods: `sort_by_time()`, `filter_tasks()`, `check_conflicts()`

- Briefly describe your initial UML design.
My app separates pet information from the scheduling logic to keep the code organized.
- What classes did you include, and what responsibilities did you assign to each?
**Owner**: Manages the owner's profile and a list of pets.
**Pet**: Stores pet details and a list of their specific tasks.
**Task**: Keeps track of one single activity, including its name, priority, and completion status.
**Scheduler**: The brain of the app that handles sorting and filtering tasks.

**b. Design changes**

- Did your design change during implementation?
Yes, my design changed significantly after running the AI skeleton review.
- If yes, describe at least one change and why you made it.
**What changed**: The AI assistant pointed out three major architectural risks: data synchronization risks between `Owner` and `Pet` tasks, tight coupling of the `Scheduler` to a single pet instance, and the absence of a start-time tracker for scheduling outputs.
**Why**: To fix these bottlenecks, I accepted the AI's recommendations to make `Pet` the single source of truth for its own tasks, decouple the `Scheduler` so it can handle multiple pets, and prepare a structured concept for tracking assigned time slots rather than passing fragile raw dictionaries around.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
It only warns us if two tasks are at the exact same time (like both at 08:30). It cannot check if a long task overlaps with a short task (like an 08:00 walk overlapping with an 08:15 feeding).
- Why is that tradeoff reasonable for this scenario?
Most pet tasks, like giving food or medicine, take only a few minutes. Checking exact time matches is simple, fast, and works well enough for a basic app.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
The file context reference feature and inline code generation were the most effective features. Keeping `pawpal_system.py` open allowed the AI to automatically read my entire codebase and seamlessly align it whenever I requested UI updates or generated UML diagrams.
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
During Phase 6, Step 2, when I asked the AI to update the UML diagram, it attempted to overwrite my initial draft file (`uml_draft.mmd`) instead of creating a new one. I rejected this action, restored my original draft using Git commands, and explicitly instructed the AI to isolate the final architecture inside a separate `uml_final.mmd` file.

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
Starting a fresh chat session for each phase kept the context clean. It prevented the AI from getting confused by old error logs and outdated logic from the testing phase, ensuring it focused entirely on the current UI polishing tasks.
- How separate chat sessions helped:** Starting a fresh chat session for each phase kept the context clean. It prevented the AI from getting confused by old error logs and outdated logic from the testing phase, ensuring it focused entirely on the current UI polishing tasks.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
While AI is an incredible coding tool and brainstorming partner, it has clear limitations—such as overlooking minor instruction details, accidentally overwriting files, or forgetting UI component placements. I learned that being a "lead architect" means stepping away from pure typing and taking full responsibility to audit, verify, and strictly control the system's direction to ensure a professional end product.
