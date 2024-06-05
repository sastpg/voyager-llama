from pathlib import Path
import re
import pandas as pd 
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

def extract_infos_and_errors(result_file: Path, task: str = 'combat')->tuple[list[dict], list[dict]]:
    with open(result_file, 'r') as f:
        data = f.read()
    lines = data.split('\n')
    infos = []
    errors = []
    # 正则表达式，提取关键信息
    if task == 'combat':
        pattern = r'Route (\d+):.*Ticks on each step: \[(.*?)\], LLM iters: (\d+), Health: (\d+\.\d+)'
        error_pattern = r'.*caused by (.*)'
    else:
        raise NotImplementedError(f"Task {task} pattern not implemented.")

    for line in lines:
        # 使用正则表达式提取信息
        
        error_info = re.search(error_pattern, line)
        if error_info:
            # print('error:', error_info.group(1))
            error = error_info.group(1)
            if error not in errors:
                errors.append(error)
        else:
            extracted_info = re.search(pattern, line)
            if extracted_info:
                route = int(extracted_info.group(1))
                last_ticks = int(extracted_info.group(2).split(',')[-1])
                llm_iters = int(extracted_info.group(3))
                health = float(extracted_info.group(4))
                infos.append({'route': route, 'last_ticks': last_ticks, 'llm_iters': llm_iters, 'health': health})
                # print(f"Route: {route}, Last Ticks: {last_ticks}, LLM iters: {llm_iters}, Health: {health}")
            else:
                print("No match found.")
    errors = [{'error': error} for error in errors]
    return infos, errors


if __name__ == '__main__':
    all_results_dir = Path(__file__).parent.parent.parent / 'results/all_results_64'
    # merge_results(all_results_dir, 'combat')
    all_errors = []
    all_infos_df = []
    for _file in (all_results_dir.parent / 'merged_results').iterdir():
        if _file.is_file() and _file.suffix == '.txt':
            infos, errors = extract_infos_and_errors(_file, 'combat')
            all_errors += errors
            all_infos_df.append(pd.DataFrame(infos).add_prefix(f'{_file.stem}_')) 
            # pd.DataFrame(errors).to_csv(_file.parent / f'{_file.stem}_errors.csv', index=False)
            # break
    pd.DataFrame(all_errors).to_csv(all_results_dir.parent / 'all_errors.csv', index=False)
    pd.concat(all_infos_df, axis=1).to_csv(all_results_dir.parent / 'all_infos.csv', index=False)


            
