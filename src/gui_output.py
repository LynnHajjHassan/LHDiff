import tkinter as tk
from tkinter import ttk
from typing import List, Dict


def run_visualizer(
    left_lines: List[str],
    right_lines: List[str],
    mapping: Dict[int, List[int]],
) -> None:
    """
    Simple GUI:
      - Left side: old file lines
      - Right side: new file lines
      - Click a left line -> corresponding right lines are highlighted

    mapping: L_index -> [list of R_indices]
    """

    root = tk.Tk()
    root.title("LHDiff – Line Mapping Visualizer (Hanan)")

    # Main horizontal layout
    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid(row=0, column=0, sticky="nsew")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

    # ---- Titles ----
    ttk.Label(main_frame, text="Old File (Left)", font=("Segoe UI", 11, "bold")).grid(
        row=0, column=0, padx=5, pady=(0, 5)
    )
    ttk.Label(main_frame, text="New File (Right)", font=("Segoe UI", 11, "bold")).grid(
        row=0, column=1, padx=5, pady=(0, 5)
    )

    # ---- Left listbox + scrollbar ----
    left_frame = ttk.Frame(main_frame)
    left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))

    right_frame = ttk.Frame(main_frame)
    right_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0))

    main_frame.rowconfigure(1, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

    # Left
    left_scroll = ttk.Scrollbar(left_frame, orient="vertical")
    left_list = tk.Listbox(
        left_frame,
        yscrollcommand=left_scroll.set,
        exportselection=False,  # keep selection even when other listbox focused
        width=60,
    )
    left_scroll.config(command=left_list.yview)
    left_list.grid(row=0, column=0, sticky="nsew")
    left_scroll.grid(row=0, column=1, sticky="ns")

    left_frame.rowconfigure(0, weight=1)
    left_frame.columnconfigure(0, weight=1)

    # Right
    right_scroll = ttk.Scrollbar(right_frame, orient="vertical")
    right_list = tk.Listbox(
        right_frame,
        yscrollcommand=right_scroll.set,
        exportselection=False,
        width=60,
        selectmode="extended",
    )
    right_scroll.config(command=right_list.yview)
    right_list.grid(row=0, column=0, sticky="nsew")
    right_scroll.grid(row=0, column=1, sticky="ns")

    right_frame.rowconfigure(0, weight=1)
    right_frame.columnconfigure(0, weight=1)

    # ---- Status label (shows mapping info) ----
    status_var = tk.StringVar()
    status_label = ttk.Label(main_frame, textvariable=status_var, anchor="w")
    status_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))

    # ---- Populate listboxes ----
    for i, line in enumerate(left_lines):
        display = f"{i:4d}: {line}"
        left_list.insert(tk.END, display)

    for j, line in enumerate(right_lines):
        display = f"{j:4d}: {line}"
        right_list.insert(tk.END, display)

    # ---- Selection callback ----
    def on_left_select(event):
        # Clear right selection first
        right_list.selection_clear(0, tk.END)

        sel = left_list.curselection()
        if not sel:
            status_var.set("No left line selected.")
            return

        l_idx = sel[0]
        mapped = mapping.get(l_idx, [])

        if not mapped:
            status_var.set(f"Left line {l_idx} has no mapping.")
            return

        # Highlight all mapped right lines
        for r_idx in mapped:
            if 0 <= r_idx < right_list.size():
                right_list.selection_set(r_idx)
                right_list.see(r_idx)

        if len(mapped) == 1:
            status_var.set(f"Left line {l_idx} → Right line {mapped[0]}")
        else:
            status_var.set(f"Left line {l_idx} → Right lines {mapped}")

    left_list.bind("<<ListboxSelect>>", on_left_select)

    root.mainloop()


# -------------- Demo when running directly --------------
if __name__ == "__main__":
    # Demo example with a split and a normal mapping
    left_demo = [
        "x = a + b;",          # line 0
        "return x;",           # line 1
        "total = a + b + c;",  # line 2
    ]

    right_demo = [
        "x = a",               # line 0
        "+ b;",                # line 1
        "return x;",           # line 2
        "total = a",           # line 3
        "+ b",                 # line 4
        "+ c;",                # line 5
    ]

    # Suppose after split detection you got:
    mapping_demo = {
        0: [0, 1],        # split
        1: [2],           # simple 1-1
        2: [3, 4, 5],     # long split
    }

    run_visualizer(left_demo, right_demo, mapping_demo)
