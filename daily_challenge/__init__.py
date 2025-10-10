import os, subprocess
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


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

    # Create a 7x53 matrix initialized with -1 (white for days not in 2025)
    heatmap = np.full((7, 53), -1)

    # Define the start and end dates for 2025
    start_date = datetime(2025, 1, 1).date()
    end_date = datetime(2025, 12, 31).date()

    # Ensure all commit dates are datetime.date objects
    if isinstance(commit_dates[0], str):
        commit_dates = [datetime.strptime(date, '%a %b %d %H:%M:%S %Y %z').date() for date in commit_dates]
    elif isinstance(commit_dates[0], datetime):
        commit_dates = [date.date() for date in commit_dates]

    # Convert commit_dates to a set for faster lookup
    commit_dates_set = set(commit_dates)

    # Filter commit dates to only include those in 2025
    commit_dates = [date for date in commit_dates if start_date <= date <= end_date]

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

    # Plot the heatmap
    plt.figure(figsize=(10, 2))  # Adjust the figure size
    from matplotlib.colors import ListedColormap, BoundaryNorm
    colormap = ListedColormap(['white', 'whitesmoke', 'chartreuse'])
    norm = BoundaryNorm([-1, 0, 1.5, 3], colormap.N)
    plt.imshow(heatmap, cmap=colormap, norm=norm, aspect='auto', interpolation='nearest')

    # Add gridlines for the frame
    sundays = [(start_date + timedelta(weeks=i) - timedelta(days=start_date.weekday()) + timedelta(days=6)).strftime('%b %d') for i in range(53)]
    plt.grid(visible=True, color='white', linewidth=0.5, linestyle='-', alpha=0.5)  # Adjust gridline color
    plt.gca().set_xticks(np.arange(-0.5, 53, 1), minor=True)
    plt.gca().set_yticks(np.arange(-0.5, 7, 1), minor=True)
    plt.gca().grid(which='minor', color='white', linestyle='-', linewidth=2)
    plt.gca().tick_params(which='minor', size=0)

    # Remove major gridlines
    plt.gca().grid(which='major', visible=False)

    # Format the plot
    num_commit_dates = len(commit_dates_set)
    plt.title(f'{num_commit_dates} successful challenge days in 2025')
    plt.yticks(ticks=range(7), labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.xticks(ticks=range(0, 53, 2), labels=sundays[::2], rotation=45, ha='right')

    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    # TODO: Heatmap size is hard coded to be (7, 53) but for leap years that start on a Sunday, we will need (7, 54)
    #       53 is hard coded in other places too. globally replace 53 with 54
    #       Leap years that starts on a Sunday: 2040, 2068, 2096, 2124. We have until 2040 to fix this.
    
    # TODO: This is how you can move to the root of a project: cd $(git rev-parse --show-toplevel)
    #       This will be needed when setting up the pre-commit hook

    # repo_path = 'D:/pyscripts/FixedIncome2025'  # Ensure this points to the root of the Git repository
    # commit_dates = get_commit_dates(repo_path)

    # draw_2025_heatmap_with_colors(commit_dates, output_file="../2025_colored_heatmap.png")

    draw_2025_heatmap()

    
