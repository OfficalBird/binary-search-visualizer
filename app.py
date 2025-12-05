import gradio as gr
# Parse the raw comma-separated string into a list of integers.
# Strips whitespace and validates that all non-empty parts are integers.
def parse_number_list(list_str: str):
    # Guard: make sure user actually typed something
    if not list_str or list_str.strip() == "":
        raise ValueError("Please enter at least one number in the list.")
    # Split on commas to get each "piece" of the list
    parts = list_str.split(",")
    numbers = []
    for p in parts:
        p = p.strip()
        # Skip empty entries like "1, , 2"
        if p == "":
            continue
        try:
            n = int(p)
        except ValueError:
            # If any part is not an integer, stop and tell the user
            raise ValueError(
                f"'{p}' is not a valid integer. Please use only whole numbers separated by commas."
            )
        numbers.append(n)

    # If after cleaning everything we still have no numbers, error out
    if len(numbers) == 0:
        raise ValueError(
            "No valid numbers were found. Please check your input and try again."
        )

    return numbers
# Run a standard binary search on a sorted list,
# while recording each step as a human-readable explanation.
def binary_search_with_steps(sorted_list, target):
    steps = []               # List of text descriptions for each step
    low = 0                  # Start of current search range
    high = len(sorted_list) - 1  # End of current search range (inclusive)
    step_num = 1             # Counter for labeling the steps

    # Continue while there is still a valid range to search
    while low <= high:
        # Middle index for the current range
        mid = (low + high) // 2
        mid_value = sorted_list[mid]
        # Build a visual line of the list, highlighting the mid element
        visual_parts = []
        for i, value in enumerate(sorted_list):
            if i == mid:
                visual_parts.append(f"[{value}]")  # Mark current mid with brackets
            else:
                visual_parts.append(str(value))
        visual_line = " ".join(visual_parts)

        # Describe the current state of the search
        step_description = (
            f"Step {step_num}:\n"
            f"  low = {low}, high = {high}, mid = {mid}, value at mid = {mid_value}\n"
            f"  List: {visual_line}\n"
        )
        steps.append(step_description)

        # Check if we found the target
        if mid_value == target:
            steps.append(f"Found {target} at index {mid} (0-based index).")
            return True, mid, steps
        # If mid value is too small, discard the left half
        elif mid_value < target:
            steps.append(f"{mid_value} < {target}, so search the right half.\n")
            low = mid + 1
        # If mid value is too large, discard the right half
        else:
            steps.append(f"{mid_value} > {target}, so search the left half.\n")
            high = mid - 1

        step_num += 1

    # If the loop exits, the target is not in the list
    steps.append(f"{target} was not found in this list.")
    return False, -1, steps
# Wrapper that parses user input, validates the target, sorts the list,
# runs binary search, and formats the output as Markdown for Gradio.
def run_binary_search(list_str: str, target_str: str, output_mode: str = "Step-by-step"):
    try:
        # Convert list input into a list of integers
        numbers = parse_number_list(list_str)

        # Validate and parse the target
        target_str = target_str.strip()
        if target_str == "":
            msg = "Please enter a target value."
            return msg, msg

        try:
            target = int(target_str)
        except ValueError:
            msg = "Target must be an integer (for example, 7)."
            return msg, msg

        # Binary search requires a sorted list, so sort a copy
        sorted_list = sorted(numbers)

        # Run the search and collect step-by-step explanations
        found, index, steps = binary_search_with_steps(sorted_list, target)

        # Intro section describing the inputs used
        intro = (
            "### Binary Search Visualizer\n"
            f"- **Original list:** {numbers}\n"
            f"- **Sorted list used for search:** {sorted_list}\n"
            f"- **Target:** {target}\n\n"
        )

        # Count how many step entries were added
        num_iterations = sum(1 for s in steps if s.startswith("Step"))

        # Build a quick summary of whether we found the target
        if found:
            result_line = (
                f"Result: Target {target} was found at index `{index}` "
                "in the sorted list."
            )
            found_text = "Yes"
        else:
            result_line = (
                f"Result: Target {target} was not found in the list."
            )
            found_text = "No"

        # High-level stats that always show in the summary box
        summary_md = (
            "### Quick stats\n\n"
            f"- **Found:** {found_text}\n"
            f"- **List length:** `{len(sorted_list)}`\n"
            f"- **Binary search iterations:** `{num_iterations}`\n"
            "- **Time complexity:** `O(log n)`\n"
        )

        # Decide how much detail to show based on the selected mode
        if output_mode == "Quick summary only":
            # Short explanation + result
            detail_md = (
                intro
                + "### Explanation\n\n"
                "Binary search keeps cutting the remaining list in half. "
                "On each iteration it compares the middle element to the target and discards "
                "either the left half or the right half.\n\n"
                + result_line
            )
        else:
            # Full step-by-step breakdown, formatted as code blocks
            steps_markdown = "### Step-by-step process:\n\n"
            for s in steps:
                steps_markdown += "```text\n" + s + "\n```\n\n"
            detail_md = intro + steps_markdown + result_line

        return summary_md, detail_md

    # Catch any unexpected error and show it in both outputs
    except Exception as e:
        msg = f"Error: {e}"
        return msg, msg
# Basic app metadata for Gradio UI
title = "Binary Search Step-by-Step Visualizer"
description = (
    "Learn how binary search works by watching the algorithm narrow down the search range.\n"
    "Enter a list of integers and a target value, then choose whether you want a full\n"
    "step-by-step explanation or just a quick summary."
)

# Define the Gradio Blocks interface
with gr.Blocks(title=title) as demo:
    # App header
    gr.Markdown(f"# {title}")
    gr.Markdown(description)

    # Quick reminder about sorting
    gr.Markdown(
        "**Tip:** Binary search only works correctly on a sorted list. "
        "This app will sort your list for you before searching."
    )

    with gr.Row():
        # Left column: user input controls
        with gr.Column(scale=1):
            gr.Markdown("### Input")

            # Textbox for entering the list of numbers
            list_input = gr.Textbox(
                label="List of numbers (comma-separated)",
                value="8, 3, 10, 2, 6, 1",
                placeholder="Example: 8, 3, 10, 2, 6, 1",
                lines=2
            )

            # Textbox for the target value to search for
            target_input = gr.Textbox(
                label="Target value (integer)",
                value="6",
                placeholder="Example: 6",
                lines=1
            )

            # Radio button to choose output style
            output_mode = gr.Radio(
                ["Step-by-step", "Quick summary only"],
                value="Step-by-step",
                label="Explain the result as"
            )

            # Buttons to run the search or clear the inputs/outputs
            run_button = gr.Button("Run Binary Search", variant="primary")
            clear_button = gr.Button("Clear", variant="secondary")

        # Right column: output display
        with gr.Column(scale=1):
            gr.Markdown("### Output")
            # Top box shows quick summary / stats
            summary_box = gr.Markdown("Run the search to see a quick summary.")
            # Bottom box shows detailed explanation (or errors)
            output_markdown = gr.Markdown("Detailed explanation will appear here.")

    # Example inputs to quickly demo the app behavior
    gr.Examples(
        examples=[
            ["8, 3, 10, 2, 6, 1", "6", "Step-by-step"],
            ["1, 2, 3, 4, 5, 6, 7", "4", "Step-by-step"],
            ["2, 4, 6, 8, 10", "5", "Quick summary only"],
        ],
        inputs=[list_input, target_input, output_mode],
        outputs=[summary_box, output_markdown],
        fn=run_binary_search,
        cache_examples=False,
        label="Try some examples"
    )

    # Wire the "Run" button to execute the binary search
    run_button.click(
        fn=run_binary_search,
        inputs=[list_input, target_input, output_mode],
        outputs=[summary_box, output_markdown]
    )

    # Wire the "Clear" button to reset inputs and outputs
    clear_button.click(
        fn=lambda: (
            "",
            "",
            "Step-by-step",
            "Run the search to see a quick summary.",
            "Detailed explanation will appear here.",
        ),
        inputs=None,
        outputs=[list_input, target_input, output_mode, summary_box, output_markdown]
    )


# Launch the Gradio app when this file is run directly
if __name__ == "__main__":
    demo.launch()
