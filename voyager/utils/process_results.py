from pathlib import Path
def merge_results(results_dir: Path, task: str):
    merge_resulst_dir = results_dir.parent / 'merged_results'
    merge_resulst_dir.mkdir(exist_ok=True, parents=True)
    for _dir in results_dir.iterdir():
        if _dir.is_dir():
            task_results_dir = _dir / 'results' / task
            if task_results_dir.exists():
                for _file in task_results_dir.iterdir():
                    if _file.is_file():
                        new_file = merge_resulst_dir / _file.name
                        # breakpoint()
                        with open(_file, 'r') as f:
                            data = f.read()
                        with open(new_file, 'a') as f:
                            f.write(data)


if __name__ == '__main__':
    all_results_dir = Path(__file__).parent.parent.parent / 'results/all_results_64'
    merge_results(all_results_dir, 'combat')
