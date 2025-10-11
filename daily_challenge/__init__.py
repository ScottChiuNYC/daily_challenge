import os, subprocess
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

def create_yearly_heatmaps_dir(repo_root: str | None = None) -> tuple[str, bool]:
    """Ensure a `yearly_heatmaps` directory exists at the repository root.

    - repo_root: optional path to the repository root. If None, try `git rev-parse --show-toplevel`.
      If git is not available, fall back to the parent directory of this package.
    - Returns: (dir_path, created) where created is True if the directory was newly created.
    """
    if repo_root is None:
        try:
            completed = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
            )
            repo_root = completed.stdout.strip()
        except Exception:
            # Fallback: parent of the package directory (project root)
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    dir_path = os.path.join(repo_root, "yearly_heatmaps")
    created = False
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        created = True
    return dir_path, created

def get_commit_dates(repo_path = '.'):
    os.chdir(repo_path)
    # Get the commit dates using git log
    result = subprocess.run(['git', 'log', '--pretty=format:%cd'], capture_output=True, text=True)
    if result.returncode == 0:
        # Split the output into a list of dates
        return result.stdout.splitlines()
    else:
        raise Exception('Error retrieving commit dates: ' + result.stderr)

def draw_2025_heatmap(commit_dates=None, output_file="./yearly_heatmaps/2025.png"):
    # Ensure the yearly_heatmaps directory exists at the project root before writing
    try:
        create_yearly_heatmaps_dir()
    except Exception:
        # If directory creation fails for any reason, continue and let save attempt raise if needed
        pass

    commit_dates = commit_dates or get_commit_dates()

    # Define start_date and end_date at the top of the function
    start_date = datetime(2025, 1, 1).date()
    end_date = datetime(2025, 12, 31).date()

    # Create a 7x53 matrix initialized with -1 (white for days not in 2025)
    heatmap = np.full((7, 53), -1)

    # Ensure all commit dates are datetime.date objects
    if isinstance(commit_dates[0], str):
        commit_dates = [datetime.strptime(date, '%a %b %d %H:%M:%S %Y %z').date() for date in commit_dates]
    elif isinstance(commit_dates[0], datetime):
        commit_dates = [date.date() for date in commit_dates]

    # Filter commit dates to only include those in 2025
    commit_dates = [date for date in commit_dates if start_date <= date <= end_date]

    # Convert commit_dates to a set for faster lookup
    commit_dates_set = set(commit_dates)

    # Iterate through all days in 2025 and populate the heatmap
    current_date = start_date
    while current_date <= end_date:
        week = ((current_date - start_date).days + start_date.weekday()) // 7
        day = current_date.weekday()

        if current_date in commit_dates_set:
            heatmap[day, week] = 2  # Chartreuse for days with a commit
        else:
            heatmap[day, week] = 1  # Whitesmoke for days in 2025 without a commit

        current_date += timedelta(days=1)

    # Plot the heatmap by drawing individual squares
    plt.figure(figsize=(10, 2))  # Adjust the figure size
    ax = plt.gca()

    # Define colors for the squares
    colors = {1: (245/255, 245/255, 245/255, 0.65), 2: (127/255, 255/255, 0, 1), -1: 'none'}

    # Define the gap size
    gap = 0.2

    # Draw each square
    for week in range(53):
        for day in range(7):
            color = colors[heatmap[day, week]]
            rect = plt.Rectangle((week + gap / 2, 6 - day + gap / 2), 1 - gap, 1 - gap, color=color, ec=None)
            ax.add_patch(rect)

    # Define Sundays for the x-axis labels
    sundays = [(start_date + timedelta(weeks=i) - timedelta(days=start_date.weekday()) + timedelta(days=6)).strftime('%b %d') for i in range(53)]

    # Calculate the number of unique commit dates
    num_commit_dates = len(commit_dates_set)

    # Set limits and aspect ratio
    ax.set_xlim(0, 53)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal', adjustable='box')

    # Position tick labels at the centers of the squares. Rectangles are drawn
    # at x=week + gap/2 with width (1-gap), so their centers are at week+0.5.
    # Similarly, y positions use 6 - day + gap/2 so centers are at 6 - day + 0.5.
    x_tick_positions = [i + 0.5 for i in range(0, 53, 2)]
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels(sundays[::2], rotation=45, ha='right')

    y_tick_positions = [6 - d + 0.5 for d in range(7)]
    ax.set_yticks(y_tick_positions)
    ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

    # Update title with a neutral color
    plt.title(f'{num_commit_dates} committed days in 2025', color='#808080')

    # Update tick labels with a neutral color
    ax.tick_params(axis='x', colors='#808080')
    ax.tick_params(axis='y', colors='#808080')

    # Update the frame color to gray
    ax.spines['top'].set_color('#808080')
    ax.spines['bottom'].set_color('#808080')
    ax.spines['left'].set_color('#808080')
    ax.spines['right'].set_color('#808080')

    # Title and layout adjustments
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2)

    # Save the heatmap with a transparent background
    plt.savefig(output_file, transparent=True)
    plt.close()


def main():
    out = Path("yearly_heatmaps") / "2025.png"
    # Ensure directory exists and run the generator
    draw_2025_heatmap()

    # If output exists, stage it so the commit includes the generated image
    if out.exists():
        subprocess.run(["git", "add", str(out)]) 


if __name__ == "__main__":
    # TODO: Heatmap size is hard coded to be (7, 53) but for leap years that start on a Sunday, we will need (7, 54)
    #       53 is hard coded in other places too. globally replace 53 with 54
    #       Leap years that start on a Sunday: 2040, 2068, 2096, 2124. We have until 2040 to fix this.
    
    # TODO: This is how you can move to the root of a project: cd $(git rev-parse --show-toplevel), needed to set up the pre-commit hook? 

    # repo_path = 'D:/pyscripts/FixedIncome2025'  # Ensure this points to the root of the Git repository
    # commit_dates = get_commit_dates(repo_path)

    # draw_2025_heatmap(commit_dates, output_file="../2025_colored_heatmap.png")

    main()

    
