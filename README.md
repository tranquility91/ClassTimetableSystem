# ClassTimetableSystem

This is a Python-based class scheduling system designed to allocate courses to teachers efficiently, with support for both rule-based logic and optimization techniques.

## Features

- 🧠 **Rule-Based Scheduling**: Uses heuristic and custom logic to assign courses to teachers.
- 📊 **Optimization Support**: Includes linear programming approaches (`grab.py`, `last.py`) to minimize workload imbalance.
- 📁 **Excel Integration**: Reads and writes `.xlsx` files for easy integration with existing workflows.
- 🌐 **FET Export**: Convert schedules to [FET](https://www.timetabling.de/) format using `fet_converter.py`.

## File Structure

| File | Purpose |
|------|---------|
| `main.py` | Main entry point using rule-based logic |
| `grab.py`, `last.py` | Alternative schedulers using linear programming |
| `table.py`, `course_allocator.py` | Core scheduling logic and course/teacher allocation |
| `data_handler.py` | Handles Excel/CSV output |
| `fet_converter.py` | Converts schedule to FET-compatible format |
| `config.py` | Contains static configuration like teacher lists |
| `test.py` | Optional test script (for development/debugging) |

## How to Run

Make sure you have Python 3 installed, then run:

```bash
python main.py
```

To try optimization-based scheduling:

```bash
python grab.py
# or
python last.py
```

## Requirements

- `pulp` (for LP optimization)
- `openpyxl` (for Excel file handling)

Install dependencies with:

```bash
pip install -r requirements.txt
```

## License

This project is open-source and licensed under the MIT License.

## Author

tranquility91
