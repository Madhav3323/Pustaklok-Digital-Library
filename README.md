# Pustaklok

This project implements the Advanced Programming Project described in the assignment.  
(Reference: AdvancedProgramming_Project.pdf)  
File: AdvancedProgramming_Project.pdf is assumed to be the assignment specification.

## Structure
- app.py - Flask backend exposing required HTTP endpoints.
- storage.py - simple JSON-backed storage helpers.
- gui.py - Tkinter frontend interacting with the backend via HTTP.
- tests/ - unit tests for backend and frontend.
- requirements.txt - minimal dependencies.

## How to run
1. Create a virtual environment and install requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the backend:
   ```bash
   python app.py
   ```
3. In another terminal, run the GUI:
   ```bash
   python gui.py
   ```

## Notes
- Data is stored in `media_store.json` in the same folder as the scripts.
- GUI expects backend at http://127.0.0.1:5000
