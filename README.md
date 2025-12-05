Author: Sherwin Dhaliwal
Course: CISC 121 – Fall 2025/26, Section 002
Project: Binary Search Visualization App

# Binary Search Step-by-Step Visualizer

A small Gradio app that visually explains how binary search works by showing each step of the algorithm as it narrows down the search range.

---

## Demo Screenshot

![Example where the target is found](screenshots/Target_found.png)

---

## Problem Breakdown & Computational Thinking

### Why Binary Search?

Binary search is a classic and efficient algorithm for finding an element in a sorted list.

Its “divide and conquer” approach — halving the search space at each step — is intuitive and visually engaging. This makes it ideal for teaching beginners, as they can clearly observe how the values of `low`, `high`, and `mid` evolve during execution.

---

### Decomposition

The problem was broken into smaller, manageable parts:

- Parse the raw input string into a Python list of integers.
- Validate input data, ensuring each value is an integer.
- Sort the list (since binary search only works on sorted sequences).
- Initialize the search range using `low` and `high` indices.
- Repeatedly:
  - Compute the middle index `mid`.
  - Compare `sorted_list[mid]` with the target value.
  - Either return the result or update `low` and `high` to narrow the range.
  - Record textual descriptions of each step for display.
- Connect the algorithm to a Gradio UI for user interaction and visualization.

---

### Pattern Recognition

Each iteration follows the same structure:

- Examine the middle element.
- Decide whether to search left, right, or stop.
- With each iteration, the search space is roughly halved.

This consistent halving explains the algorithm’s time complexity: `O(log n)`, compared to `O(n)` for linear search.

---

### Abstraction

Low level implementation details are hidden from the user (for example, input parsing and internal indexing). Instead, the interface emphasizes:

- The original input list.
- The sorted version of the list.
- Current values of `low`, `high`, and `mid`.
- A visual representation highlighting the middle element in `[ ]`.

The user doesn’t need to worry about background logic such as error handling or Markdown formatting.

---

### Algorithm Design (Input → Processing → Output)

#### Input (GUI)

- Textbox for a comma separated list of integers.
- Textbox for the target integer to search for.
- Radio button to choose between **“Step by step”** mode or **“Quick summary only”**.

#### Processing

- Convert input strings into a validated list of integers.
- Sort the list and run the binary search while recording each iteration.
- Count and display the number of iterations.

#### Output (GUI)

A **Quick Stats** section showing:

- Whether the target was found.
- List length.
- Number of iterations.
- Time complexity `O(log n)`.

A **detailed explanation** view that provides either:

- A full step by step trace (in code blocks), or  
- A concise summary with final results.

*(Optional: include a simple flowchart image here illustrating the main binary search loop.)*

---

## Running the Project Locally

1. Clone or download this repository.
2. (Optional) Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On macOS/Linux
   # On Windows:
   # venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the Gradio app:
   python app.py

## Testing:
Some of the test cases I used to verify correctness:

| Original list       | Target | Sorted list           | Expected result                 |
| ------------------- | ------ | --------------------- | ------------------------------- |
| `1, 3, 5, 7, 9`     | `5`    | `[1, 3, 5, 7, 9]`     | Found at index 2                |
| `10, 2, 4, 6`       | `2`    | `[2, 4, 6, 10]`       | Found at index 0                |
| `4, 1, 8, 9`        | `9`    | `[1, 4, 8, 9]`        | Found at last index             |
| `2, 4, 6, 8`        | `5`    | `[2, 4, 6, 8]`        | Not found                       |
| `7`                 | `7`    | `[7]`                 | Found at index 0                |
| `7`                 | `3`    | `[7]`                 | Not found                       |
| `8, 3, 10, 2, 6, 1` | `6`    | `[1, 2, 3, 6, 8, 10]` | Found at index of the value `6` |

### Visual Examples

**1. Target found**

![Target found example](screenshots/Target_found.png)

**2. Target not found**

![Target not found example](screenshots/Target_not_found.png)

**3. Edge case (single element list)**

![Single element edge case](screenshots/Edge_case.png)

**4. Invalid input handling**

![Invalid input error message](screenshots/Invalid_input.png)

## Hugging Face Deployment

Public Space URL:

https://huggingface.co/spaces/Sherwin/binary-search-visualizer
